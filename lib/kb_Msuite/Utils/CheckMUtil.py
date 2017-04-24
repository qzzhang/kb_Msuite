# -*- coding: utf-8 -*-
import time
import json
import os
import uuid
import errno
import subprocess
import sys
import shutil
import ast

from pprint import pprint

from KBaseReport.KBaseReportClient import KBaseReport
from DataFileUtil.DataFileUtilClient import DataFileUtil

from kb_Msuite.Utils.DataStagingUtils import DataStagingUtils

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))
    sys.stdout.flush()



class CheckMUtil:
    #CHECKM_WORKFLOW_PATH = '/kb/deployment/bin/CheckMBin'
    CHECKM_WORKFLOW_PATH = '/usr/local/bin'
    CHECKM_PROCACULATED_DATA_PATH = '/data/checkm_data/'

    def _validate_run_checkM_params(self, params):
        """
        _validate_run_checkM_params:
                validates params passed to run_checkM method
        """
        log('Start validating run_checkM params')

        # check for required parameters
        for p in ['checkM_cmd_name', 'bin_folder', 'out_folder']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _process_universal_options(self, command_list, options):
        if options.get('thread'):
            command_list.append('-t')
            command_list.append(str(options.get('thread')))


    def _validate_options(self, options,
                          checkBin=False,
                          checkOut=False,
                          checkPlots=False,
                          checkTetraFile=False,
                          subcommand=''):
        if checkBin and 'bin_folder' not in options:
            raise ValueError('cannot run checkm ' + subcommand + ' without bin_folder option set')
        if checkOut and 'out_folder' not in options:
            raise ValueError('cannot run checkm ' + subcommand + ' without bin_folder option set')
        if checkPlots and 'plots_folder' not in options:
            raise ValueError('cannot run checkm ' + subcommand + ' without plots_folder option set')
        if checkTetraFile and 'tetra_file' not in options:
            raise ValueError('cannot run checkm ' + subcommand + ' without tetra_file option set')


    def _build_command(self, subcommand, options):

        command = ['checkm', subcommand]
        self._process_universal_options(command, options)

        if subcommand == 'lineage_wf':
            self._validate_options(options, checkBin=True, checkOut=True, subcommand='lineage_wf')
            if 'reduced_tree' in options and options['reduced_tree'] == 1:
                command.append('--reduced_tree')
            command.append(options['bin_folder'])
            command.append(options['out_folder'])

        elif subcommand == 'bin_qa_plot':
            self._validate_options(options, checkBin=True, checkOut=True, checkPlots=True, subcommand='bin_qa_plot')
            command.append(options['out_folder'])
            command.append(options['bin_folder'])
            command.append(options['plots_folder'])

        elif subcommand == 'dist_plot':
            self._validate_options(options, checkBin=True, checkOut=True, checkPlots=True, checkTetraFile=True,
                                   subcommand='dist_plot')
            command.append(options['out_folder'])
            command.append(options['bin_folder'])
            command.append(options['plots_folder'])
            command.append(options['tetra_file'])
            if 'dist_value' not in options:
                raise ValueError('cannot run checkm dist_plot without dist_value option set')
            command.append(str(options['dist_value']))

        else:
            raise ValueError('Invalid or unsupported checkM subcommand: ' + str(subcommand))

        return command


    def run_checkM(self, subcommand, options):
        command = self._build_command(subcommand, options)
        log('Running: ' + ' '.join(command))

        p = subprocess.Popen(command, cwd=self.scratch, shell=False)
        exitCode = p.wait()

        if (exitCode == 0):
            log('Executed command: ' + ' '.join(command) + '\n' +
                'Exit Code: ' + str(exitCode))
        else:
            raise ValueError('Error running command: ' + ' '.join(command) + '\n' +
                             'Exit Code: ' + str(exitCode))







    def _generate_report(self, result_folder, params):
        """
        generate_report: generate summary report
        """
        log('Generating report')

        uuid_string = str(uuid.uuid4())
        upload_message = 'Job Finished\n\n'

        file_list = os.listdir(result_folder)
        header = params.get('checkM_cmd_name')

        upload_message += '--------------------------\nSummary:\n\n'

        upload_message += '\n--------------------------\nOutput files for this run:\n\n'

        upload_message += "All checkM results of this run are saved in :" + result_folder

        log('Report message:\n{}'.format(upload_message))

        report_params = {
              'message': upload_message,
              'summary_window_height': 166.0,
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_Msuite_report_' + uuid_string
        }

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output


    def __init__(self, config):
        self.config = config
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']



    def package_folder(self, folder_path, zip_file_name, zip_file_description):
        dfu = DataFileUtil(self.callback_url)
        output = dfu.file_to_shock({'file_path': folder_path,
                                    'make_handle': 0,
                                    'pack': 'zip'})
        return {'shock_id': output['shock_id'],
                'name': zip_file_name,
                'description': zip_file_description}



    def copy_no_error(self, src_folder, filename, dest_folder):
        src = os.path.join(src_folder, filename)
        dest = os.path.join(dest_folder, filename)
        log('copying ' + src + ' to ' + dest)
        try:
            shutil.copy(src, dest)
        except:
            # TODO: add error message reporting
            log('copy failed')



    def build_critical_output(self, output_folder):
        crit_out_dir = os.path.join(self.scratch, 'critical_output_' + str(uuid.uuid4()))
        os.makedirs(crit_out_dir)

        self.copy_no_error(output_folder, 'lineage.ms', crit_out_dir)

        os.makedirs(os.path.join(crit_out_dir, 'storage'))
        self.copy_no_error(output_folder, os.path.join('storage', 'bin_stats.analyze.tsv'), crit_out_dir)
        self.copy_no_error(output_folder, os.path.join('storage', 'bin_stats.tree.tsv'), crit_out_dir)
        self.copy_no_error(output_folder, os.path.join('storage', 'bin_stats_ext.tsv'), crit_out_dir)
        self.copy_no_error(output_folder, os.path.join('storage', 'marker_gene_stats.tsv'), crit_out_dir)
        self.copy_no_error(output_folder, os.path.join('storage', 'tree', 'concatenated.tre'), crit_out_dir)

        return self.package_folder(crit_out_dir, 'selected_output.zip', 'Selected output from the CheckM analysis.')



    def build_html_output(self, plots_folder, output_folder, object_name):
        '''
        Based on the output of a checkM lineage run, build the output HTML report
        '''


        html_dir = os.path.join(self.scratch, 'html_' + str(uuid.uuid4()))
        os.makedirs(html_dir)

        # move plots we need into the html directory
        plot_name = 'bin_qa_plot.png'
        shutil.copy(os.path.join(plots_folder, plot_name), os.path.join(html_dir, plot_name))


        # write the report
        html = open(os.path.join(html_dir, 'report.html'), 'w')
        html.write('<html><head><title>CheckM Report for ' + object_name + '</title></head>\n')
        html.write('<body>\n')

        # include the single main summary figure
        html.write('<img src="' + plot_name + '" width="90%" />')

        html.write('<br><br><br>')

        # print out the info table
        self.build_summary_table(output_folder, html)

        html.write('</body></html>\n')
        html.close()

        return self.package_folder(html_dir, 'report.html', 'Assembled report from CheckM')





    def build_summary_table(self, output_folder, html):

        stats_file = os.path.join(output_folder, 'storage', 'bin_stats_ext.tsv')
        if not os.path.isfile(stats_file):
            log('Warning! no stats file found (looking at: ' + stats_file + ')')
            return

        bin_stats = []
        with open(stats_file) as lf:
            for line in lf:
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                col = line.split('\t')
                bin_id = col[0]
                data = ast.literal_eval(col[1])
                bin_stats.append({'bid': bin_id, 'data': data})


        fields = [{'id': 'marker lineage', 'display': 'Marker Lineage'},
                  {'id': '# genomes', 'display': '# Genomes'},
                  {'id': '# markers', 'display': '# Markers'},
                  {'id': '# marker sets', 'display': '# Marker Sets'},
                  {'id': '0', 'display': '0'},
                  {'id': '1', 'display': '1'},
                  {'id': '2', 'display': '2'},
                  {'id': '3', 'display': '3'},
                  {'id': '4', 'display': '4'},
                  {'id': '5+', 'display': '5+'},
                  {'id': 'Completeness', 'display': 'Completeness'},
                  {'id': 'Contamination', 'display': 'Contamination'}]

        # header
        tdStyle = ' style="border: 1px solid black; text-align: left; padding: 8px;"'
        tableStyle = ' style="border: 1px solid black; border-collapse: collapse"'

        html.write('<table' + tableStyle + '>\n')
        html.write('  <tr>\n')
        html.write('    <th' + tdStyle + '><b>Bin Name</b></th>\n')
        for f in fields:
            html.write('    <th' + tdStyle + '>' + f['display'] + '</th>\n')
        html.write('  </tr>\n')

        for b in bin_stats:
            html.write('  <tr>\n')
            html.write('    <td' + tdStyle + '>' + b['bid'] + '</td>\n')
            for f in fields:
                html.write('    <td' + tdStyle + '>' + str(b['data'][f['id']]) + '</td>\n')
            html.write('  </tr>\n')

        html.write('</table>\n')





    def run_checkM_lineage_wf(self, params):
        '''
        Main entry point for running the lineage_wf as a KBase App
        '''

        if 'input_ref' not in params:
            raise ValueError('input_ref field was not set in params for run_checkM_lineage_wf')
        if 'workspace_name' not in params:
            raise ValueError('workspace_name field was not set in params for run_checkM_lineage_wf')


        # 1) stage input data
        dsu = DataStagingUtils(self.config)
        input_dir = dsu.stage_input(params['input_ref'], 'fna')['input_dir']
        output_dir = os.path.join(self.scratch, 'output_' + os.path.basename(input_dir))
        plots_dir = os.path.join(self.scratch, 'plot_' + os.path.basename(input_dir))
        log('Staged input directory: ' + input_dir)


        # 2) run the lineage workflow
        lineage_wf_options = {'bin_folder': input_dir,
                              'out_folder': output_dir,
                              'thread': 2,
                              'reduced_tree': 1
                              }
        self.run_checkM('lineage_wf', lineage_wf_options)


        # 3) build the plots
        bin_qa_plot_options = {'bin_folder': input_dir,
                               'out_folder': output_dir,
                               'plots_folder': plots_dir
                               }
        self.run_checkM('bin_qa_plot', bin_qa_plot_options)



        # 4) package download files
        direct_download_files = []
        if 'save_output_dir' in params and str(params['save_output_dir']) == '1':
            log('packaging full output directory')

            zipped_output_file = self.package_folder(output_dir, 'full_output.zip', 'Full output of CheckM')
            direct_download_files.append(zipped_output_file)
        else:
            log('not packaging full output directory, selecting specific files')
            direct_download_files.append(self.build_critical_output(output_dir))

        if 'save_plots_dir' in params and str(params['save_plots_dir']) == '1':
            log('packaging output plots directory')
            zipped_output_file = self.package_folder(plots_dir, 'plots.zip', 'Output plots from CheckM')
            direct_download_files.append(zipped_output_file)
        else:
            log('not packaging output plots directory')


        # 5) build the HTML report
        html_zip = self.build_html_output(plots_dir, output_dir, params['input_ref'])


        # 6) save report
        report_params = {'message': '',
                         'direct_html_link_index': 0,
                         'html_links': [html_zip],
                         'file_links': direct_download_files,
                         'report_object_name': 'kb_checkM_report_' + str(uuid.uuid4()),
                         'workspace_name': params['workspace_name']
                         }

        kr = KBaseReport(self.callback_url)
        report_output = kr.create_extended_report(report_params)

        return {'report_name': report_output['name'],
                'report_ref': report_output['ref']}

