import time
import json
import os
import uuid
import errno
import subprocess
import shutil
import sys
import re

from KBaseReport.KBaseReportClient import KBaseReport

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class CheckMUtil:
    CHECKM_TOOLKIT_PATH = '/kb/deployment/bin/CheckM'

    def _validate_run_checkM_params(self, params):
        """
        _validate_run_checkM_params:
                validates params passed to run_checkM method
        """
        log('Start validating run_checkM params')

        # check for required parameters
        for p in ['checkM_workflow_name', 'putative_genomes_folder', 'workspace_name', 'file_extension']:
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

    def _fetch_summary(self, output):
        """
        _fetch_summary: fetch summary info from output
        """
        log('Starting fetch summary report')
        start = '========== Job finished =========='
        end = '========== Elapsed Time =========='
        self.output_summary = ''

        if len(output.split(start)) > 1:
            self.output_summary = output.split(start)[1].split(end)[0]

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            self._fetch_summary(output)
            log('Executed commend:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running commend:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _generate_report(self, result_directory, params):
        """
        generate_report: generate summary report
        """
        log('Generating report')

        uuid_string = str(uuid.uuid4())
        upload_message = 'Job Finished\n\n'

        file_list = os.listdir(result_directory)
        header = params.get('out_header')

        upload_message += '--------------------------\nSummary:\n\n'

        if header + '.summary' in file_list:
            with open(os.path.join(result_directory, header + '.summary'), 'r') as summary_file:
                lines = summary_file.readlines()
                for line in lines:
                    line_list = line.split('\t')
                    if len(line_list) == 5:
                        upload_message += '{:{number}} {:10} {:15} {:15} {}'.format(
                                                            line_list[0], line_list[1],
                                                            line_list[2], line_list[3],
                                                            line_list[4], number=len(header)+12)
                    elif len(line_list) == 4:
                        upload_message += '{:{number}} {:15} {:15} {}'.format(
                                                            line_list[0], line_list[1],
                                                            line_list[2], line_list[3],
                                                            number=len(header)+12)
                    else:
                        upload_message = upload_message.replace(
                                                '--------------------------\nSummary:\n\n', '')
        if self.output_summary:
            upload_message += self.output_summary
        else:
            upload_message += '\n--------------------------\nOutput files for this run:\n\n'
            if header + '.summary' in file_list:
                upload_message += 'Summary file: {}.summary\n'.format(header)
                file_list.remove(header + '.summary')

            if header + '.abundance' in file_list:
                upload_message += 'Genome abundance info file: {}.abundance\n'.format(header)
                file_list.remove(header + '.abundance')

            if header + '.marker' in file_list:
                upload_message += 'Marker counts: {}.marker\n'.format(header)
                file_list.remove(header + '.marker')

            if header + '.marker_of_each_bin.tar.gz' in file_list:
                upload_message += 'Marker genes for each bin: '
                upload_message += '{}.marker_of_each_bin.tar.gz\n'.format(header)
                file_list.remove(header + '.marker_of_each_bin.tar.gz')

            if header + '.001.fasta' in file_list:
                upload_message += 'Bin files: '
                bin_file = []
                for file_name in file_list:
                    if re.match(header + '\.\d{3}\.fasta', file_name):
                        bin_file.append(file_name)

                bin_file.sort()
                upload_message += '{} - {}\n'.format(bin_file[0], bin_file[-1])
                file_list = [item for item in file_list if item not in bin_file]

            if header + '.noclass' in file_list:
                upload_message += 'Unbinned sequences: {}.noclass\n'.format(header)
                file_list.remove(header + '.noclass')

            if header + '.tooshort' in file_list:
                upload_message += 'Short sequences: {}.tooshort\n'.format(header)
                file_list.remove(header + '.tooshort')

            if header + '.log' in file_list:
                upload_message += 'Log file: {}.log\n'.format(header)
                file_list.remove(header + '.log')

            if header + '.marker.pdf' in file_list:
                upload_message += 'Visualization file: {}.marker.pdf\n'.format(header)
                file_list.remove(header + '.marker.pdf')

            if file_list:
                upload_message += 'Other files:\n{}'.format('\n'.join(file_list))

        log('Report message:\n{}'.format(upload_message))

        report_params = {
              'message': upload_message,
              'summary_window_height': 166.0,
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_maxbin_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        self.shock_url = config['shock-url']

    def run_checkM(self, params):
        """
        required params:
        putative_genomes_folder: folder path that holds all putative genome files with (fa as the file extension) to be checkM-ed
        checkM_workflow_name: name of the CheckM workflow,e.g., lineage_wf or taxonomy_wf
        file_extension: the extension of the putative genome file, should be "fna"
        workspace_name: the name of the workspace it gets saved to.

        optional params:
        thread: number of threads; default 1
        external_genes: indicating an external gene call instead of using prodigal, default 0
        external_genes_file: the file containing genes for gene call, default "" 

        markerset: choose between 107 marker genes by default or 40 marker genes
        min_contig_length: minimum contig length; default 1000
        plotmarker: specify this option if you want to plot the markers in each contig

        ref: https://github.com/Ecogenomics/CheckM/wiki/Installation#how-to-install-checkm
        """
        log('--->\nrunning MaxBinUtil.run_maxbin\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_checkM_params(params)
        
        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        for file in new_files:
            shutil.copy(file, result_directory)

        log('Saved result files to: {}'.format(result_directory))
        log('Generated files:\n{}'.format('\n'.join(os.listdir(result_directory))))

        reportVal = self._generate_report(result_directory, params)

        returnVal = {
            'result_directory': result_directory,
            'obj_ref': 'obj_ref'
        }

        returnVal.update(reportVal)

        return returnVal

