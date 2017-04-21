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

    # Lineage-specific Workflow
    def _tree(self, bin_folder, out_folder):
        """
        The checkm ‘tree’ command places genome bins into a reference genome tree. 
        All genomes to be analyzed must reside in a single ‘bins’ directory. 
        CheckM assumes genome bins are in FASTA format with the extension ‘fna’, 
        though this can be changed with the –x flag. 
        """


    def _tree_qa(self, out_folder):
        """
        The checkm ‘tree_qa’ command indicates the number of phylogenetically informative
        marker genes found in each genome bin along with a taxonomic string indicating 
        its approximate placement in the tree. If desired, genome bins with few phylogenetically 
        marker genes may be removed in order to reduce the computational requirements of 
        the following commands.
        Alternatively, if only genomes from a particular taxonomic group are of interest 
        these can be moved to a separate directory and analysed separately.
        """


    def _lineage_set(self, out_folder, marker_file):
        """
        The checkm ‘lineage_set’ command creates a marker file indicating lineage-specific marker sets
        suitable for evaluating each genome. This marker file is passed to the ‘analyze’ command.
        """


    def _analyze(self, marker_file, bin_folder, out_folder):
        """
        The checkm ‘analyze’ command takes in a marker file,  identify marker genes and estimate the
        completeness and contamination of each genome bin.
        """


    def _qa(self, marker_file, out_folder):
        """
        The checkm ‘qa’ command produces different tables summarizing the quality of each genome bin.
        """

    def _lineage_wf(self, bin_folder, out_folder, thread=8):
        """
        Runs tree, lineage_set, analyze, qa

    positional arguments:
        bin_folder--folder containing bins (fasta format)
        out_folder--folder to write output files

    Examples:
                1) generic:
                   checkm lineage_wf ./bins ./output
                2) to processes these genomes with 8 threads
                   checkm lineage_wf -t 8 -x fa /path/to/source/bins /path/to/save/checkm/results
                3) to process files of called genes in amino acid space which have the extension faa:
                   checkm lineage_wf --genes -t 8 -x faa <bin folder> <output folder>
    """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'checkM_cmd_name': 'lineage_wf',
            'thread': thread
        })
        self._run_command(command)


    # CheckM Plots
    def _bin_qa_plot(self, out_folder, bin_folder, plot_folder):
        """
        Bar plot of bin completeness, contamination, and strain heterogeneity.

        Provides a visual representation of the completeness, contamination, and strain
heterogeneity within each genome bin. Bars in green represent markers identified exactly once,
while bars in grey represent missing markers. Markers identified multiple times in a genome bin are
represented by shades of blue or red depending on the amino acid identity (AAI) between pairs of
multi-copy genes and the total number of copies present (2-5+). Pairs of multi-copy genes with an
AAI ≥90% are indicated with shades of blue, while genes with less amino acid similarity are shown in
red. A gene present 3 or more times may have pairs with an AAI ≥90% and pairs with an AAI < 90%. 

        positional arguments:
          out_folder--folder specified during qa command
          bin_folder--folder containing bins to plot (fasta format)
          plot_folder--folder to hold plots

        optional arguments:
          image_type {eps,pdf,png,ps,svg}--desired image type (default: png)
          dpi DPI--desired DPI of output image (default: 600)
          font_size FONT_SIZE--Desired font size (default: 8)
          x, extension EXTENSION--extension of bins (other files in folder are ignored) (default: fna)
          width WIDTH--width of output image (default: 6.5)
          row-height ROW-HEIGHT--height of each row in the output image (default: 0.3)
          w, --gc_window_size GC_WINDOW_SIZE--window size used to calculate GC histogram (default: 5000)
          ignore_hetero--do not plot strain heterogeneity
          aai_strain AAI_STRAIN--AAI threshold used to identify strain heterogeneity (default: 0.9)
          q, --quiet--suppress console output

          Example checkm bin_qa_plot ./output ./bins ./plots
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'plot_folder': plot_folder,
            'checkM_cmd_name': 'bin_qa_plot'
        })
        self._run_command(command)


    def _gc_plot(self, bin_folder, plot_folder, dist_value=95):
        """
        Create GC histogram and delta-GC plot.

        Provides a 3 pane plot suitable for assessing the GC distribution of sequences within a
genome bin. The first pane is a histogram of the number of non-overlapping 5 kbp windows with a
give percent GC. A typical genome will produce a unimodal distribution. The bimodal distribution in
this example suggests this genome bin may be substantially contaminated. The second pane plots
each sequence in the genome bin as a function of its change for the average GC of the entire
genome (x-axis) and sequence length (y-axis). The dashed red lines indicate the expected deviation
from the mean GC as a function of length. This expected deviation is pre-calculated for a set of
reference genomes and the exact percentile plotted is provided as an argument to this command. 
        
        positional arguments:
          bin_folder--folder containing bins to plot (fasta format)
          plot_folder--folder to hold plots
          dist_value--reference distribution(s) to plot; integer between 0 and 100

        optional arguments:
          image_type {eps,pdf,png,ps,svg}--desired image type (default: png)
          dpi DPI--desired DPI of output image (default: 600)
          font_size FONT_SIZE--Desired font size (default: 8)
          x, extension EXTENSION--extension of bins (other files in folder are ignored) (default: fna)
          width WIDTH--width of output image (default: 6.5)
          height HEIGHT--height of output image (default: 3.5)
          w, --gc_window_size GC_WINDOW_SIZE--window size used to calculate GC histogram (default: 5000)
          b, --gc_bin_width GC_BIN_WIDTH--width of GC bars in histogram (default: 0.01)
          q, --quiet--suppress console output
        
          Example: checkm gc_plot ./bins ./plots 95
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'plot_folder': plot_folder,
            'dist_value': dist_value,
            'checkM_cmd_name': 'gc_plot'
        })
        self._run_command(command)

    def _coding_plot(self, out_folder, bin_folder, plot_folder, dist_value=95):
        """
        Create coding density (CD) histogram and delta-CD plot.

        Provides a plot analogous to the gc_plot suitable for assessing the coding density of
sequences within a genome bin

        Example: checkm coding_plot ./output ./bins ./plots 95
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'plot_folder': plot_folder,
            'dist_value': dist_value,
            'checkM_cmd_name': 'coding_plot'
        })
        self._run_command(command)

    def _tetra_plot(self, out_folder, bin_folder, plot_folder, tetra_profile, dist_value=95):
        """
        Create tetranucleotide distance (TD) histogram and delta-TD plot.

        Provides a plot analogous to the gc_plot suitable for assessing the tetranucleotide
signatures of sequences within a genome bin. The Manhattan distance is used for determine the
different between each sequences tetranucleotide signature and the tetranucleotide signature of
the entire genome bin. This plot requires a file indicating the tetranucleotide signature of all
sequences within the genome bins. This file can be creates with the ‘tetra’ command.

        Example: checkm tetra_plot ./output ./bins ./plots tetra.tsv 95
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'plot_folder': plot_folder,
            'tetra_profile': tetra_profile,
            'dist_value': dist_value,
            'checkM_cmd_name': 'tetra_plot'
        })
        self._run_command(command)


    def _dist_plot(self, out_folder, bin_folder, plot_folder, tetra_profile, dist_value=95):
        """
        Create image with GC, CD, and TD distribution plots together.

        Produces a single figure combining the plots produced by gc_plot, coding_plot, and
tetra_plot. This plot requires a file indicating the tetranucleotide signature of all sequences within
the genome bins. This file can be created with the ‘tetra’ command.

        Example: checkm dist_plot ./output ./bins ./plots tetra.tsv 95
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'plot_folder': plot_folder,
            'tetra_profile': tetra_profile,
            'dist_value': dist_value,
            'checkm_cmd_name': 'dist_plot'
        })
        self._run_command(command)


    def _nx_plot(self, bin_folder, plot_folder):
        """
        Create Nx-plots.

        Produces a plot indicating the Nx value of a genome bin for all values of x. This provides a
more comprehensive view of the quality of an assembly than simply considering N50.
        
        Example: checkm nx_plot ./bins ./plots
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'plot_folder': plot_folder,
            'checkM_cmd_name': 'nx_plot'
        })
        self._run_command(command)


    def _len_plot(self, bin_folder, plot_folder):
        """
        Cumulative sequence length plot.

        Produces a plot of the cumulative sequence length of a genome bin with sequences
organized from longest to smallest. This provides additional information regarding the quality of an
assembled genome.

        Example: checkm len_plot ./bins ./plots
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'plot_folder': plot_folder,
            'checkm_cmd_name': 'len_plot'
        })
        self._run_command(command)


    def _len_hist(self, bin_folder, plot_folder):
        """
        Sequence length histogram.

        Produces a histogram of the number of sequences within a genome bin at different
sequence length intervals. This provides additional information regarding the quality of an
assembled genome.

        Example: checkm len_hist ./bins ./plots
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'plot_folder': plot_folder,
            'checkm_cmd_name': 'len_hist'
        })
        self._run_command(command)


    def _marker_plot(self, out_folder, bin_folder, plot_folder):
        """
        Plot position of marker genes on sequences.

        Plots the position of marker genes on sequences within a genome bin. This provides
information regarding the extent to which marker genes are collocated. The number of marker
genes within a fixed size window (2.8 kbps in this example) is indicated by with different colours.
Sequences without any marker genes are not shown. 

        Example: checkm marker_plot ./output ./bins ./plots
        """
        command = self._generate_command({
            'plot_folder': plot_folder,
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'checkm_cmd_name': 'marker_plot'
        })
        self._run_command(command)


    def _par_plot(self, out_folder, bin_folder, plot_folder, coverage_file):
        """
        Parallel coordinate plot of GC and coverage.

        Produces a parallel coordinate plot illustrating the GC and coverage of each sequence
within a genome bin. In a typical genome, all sequences will produce a similar path across the plot.
Sequences with a divergent path may be contamination. In this example, the scaffolds were
obtained from a single metagenomic dataset resulting in a single coverage dimension making it
difficult to determine if any sequences might represent contamination. This plot requires a file 
10 of 11
indicating the coverage profile of all sequences within the genome bins. This file can be creates with
the ‘coverage’ command.

        Example: checkm par_plot ./output ./bins ./plots coverage.tsv
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'plot_folder': plot_folder,
            'coverage_file': coverage_file,
            'checkm_cmd_name': 'par_plot'
        })
        self._run_command(command)


    def _cov_pca(self, bin_folder, plot_folder, coverage_file):
        """
        PCA plot of coverage profiles.

        Produces a principal component plot (PCA) of the coverage profile distance between
sequences within a putative genome. This plot requires a file indicating the coverage profile of all
sequences within the genome bins. This file can be creates with the ‘coverage’ command.

        Example: checkm cov_pca ./bins ./plots coverate.tsv
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'plot_folder': plot_folder,
            'coverage_file': coverage_file,
            'checkm_cmd_name': 'cov_pca'
        })
        self._run_command(command)

    def _tetra_pca(self, bin_folder, plot_folder, tetra_profile):
        """
        PCA plot of tetranucleotide signatures.

        Produces a principal component plot (PCA) indicating the tetranucleotide distance
between sequences within a putative genome. This plot requires a file indicating the tetranucleotide
signature of all sequences within the genome bins. This file can be creates with the ‘tetra’ command.

        Example: checkm tetra_pca ./bins ./plots tetra.tsv
        """
        command = self._generate_command({
            'bin_folder': bin_folder,
            'plot_folder': plot_folder,
            'tetra_profile': tetra_profile,
            'checkm_cmd_name': 'tetra_pca'
        })
        self._run_command(command)

    def _generate_command(self, params):
        """
        _generate_command: generate checkm command
        """

        command = ['checkm']

        cmd_name = params.get('checkM_cmd_name')
        if (cmd_name):
            command.append(cmd_name)

            if 'reduced_tree' in params and params.get('reduced_tree') == 1:
                command.append('--reduced_tree')

            if params.get('thread'):
                command.append('-t')
                command.append(str(params.get('thread')))

            """ The lineage_wf workflow command
                Example: checkm lineage_wf ./bins ./output
            """
            if(cmd_name == 'lineage_wf'):
                command.append(params.get('bin_folder'))
                command.append(params.get('out_folder'))

            """ The taxonomy_wf workflow command,
                Example: checkm taxonomy_wf domain Bacteria ./bins ./output
            """
            if(cmd_name == 'taxonomy_wf'):
                command.append('domain')
                command.append(params.get('domain'))
                command.append(params.get('bin_folder'))
                command.append(params.get('out_folder'))

            """ The bin_qa_plot command
                Example: checkm bin_qa_plot ./output ./bins ./plots
            """
            if(cmd_name == 'bin_qa_plot'):
                command.append(params.get('out_folder'))
                command.append(params.get('bin_folder'))
                command.append(params.get('plots_folder'))

            """ The gc_plot command
                Example: checkm gc_plot ./bins ./plots 95
            """
            if(cmd_name == 'gc_plot'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('dist_value'))

            """ The coding_plot command
                Example: checkm coding_plot ./output ./bins ./plots 95
            """
            if(cmd_name == 'coding_plot'):
                command += ' {}' . format(params.get('out_folder'))
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('dist_value'))

            """ The tetra_plot command
                Example: checkm tetra_plot ./output ./bins ./plots tetra.tsv 95
            """
            if(cmd_name == 'tetra_plot'):
                command += ' {}' . format(params.get('out_folder'))
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('tetra_profile'))
                command += ' {}' . format(params.get('dist_value'))

            """ The dist_plot command
                Example: checkm dist_plot ./output ./bins ./plots tetra.tsv 95
            """
            if(cmd_name == 'dist_plot'):
                command += ' {}' . format(params.get('out_folder'))
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('tetra_profile'))
                command += ' {}' . format(params.get('dist_value'))

            """ The nx_plot command
                Example: checkm nx_plot ./bins ./plots
            """
            if(cmd_name == 'nx_plot'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))

            """ The len_plot command
                Example: checkm len_plot ./bins ./plots
            """
            if(cmd_name == 'len_plot'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))

            """ The len_hist command
                Example: checkm len_hist ./bins ./plots
            """
            if(cmd_name == 'len_hist'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))

            """ The marker_plot command
                Example: checkm marker_plot ./output ./bins ./plots
            """
            if(cmd_name == 'marker_plot'):
                command += ' {}' . format(params.get('out_folder'))
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))

            """ The par_plot command
                Example: checkm par_plot ./output ./bins ./plots coverage.tsv
            """
            if(cmd_name == 'par_plot'):
                command += ' {}' . format(params.get('out_folder'))
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('coverage_file'))

            """ The cov_pca command
                Example: checkm cov_pca ./bins ./plots coverage.tsv
            """
            if(cmd_name == 'cov_pca'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('coverage_file'))

            """ The tetra_pca command
                Example: checkm tetra_pca ./bins ./plots tetra.tsv
            """
            if(cmd_name == 'tetra_pca'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('plot_folder'))
                command += ' {}' . format(params.get('tetra_profile'))
        else:
            command = 'Unrecognizable checkM command'


        return command

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """
        log('Running: ' + ' '.join(command))

        p = subprocess.Popen(command, cwd=self.scratch, shell=False)
        exitCode = p.wait()

        if (exitCode == 0):
            log('Executed command:\n{}\n'.format(command) +
                'Exit Code: {}\n'.format(exitCode))
        else:
            error_msg = 'Error running command:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\n'.format(exitCode)
            raise ValueError(error_msg)


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

    def run_checkM(self, params):
        """
        run_checkM: run the checkm commands

        required params:
        bin_folder: folder path that holds all putative genome files with (fna as the file extension) to be checkM-ed
        out_folder: folder path that holds all the checkm workflow results
        checkM_cmd_name: name of the CheckM command,e.g., lineage_wf or taxonomy_wf
        workspace_name: the name of the workspace it gets saved to.

        optional params:
        thread: number of threads; default 1
        """
        log('--->\nrunning CheckMUtil.run_checkM\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_checkM_params(params)

        result_folder = os.path.join(self.scratch, params.get('out_folder'))
        self._mkdir_p(result_folder)
        params['out_folder'] = result_folder

        command = self._generate_command(params)

        self._run_command(command)

        reportVal = self._generate_report(result_folder, params)

        returnVal = {
            'checkM_results_folder': result_folder,
            'report_ref': 'report_ref',
            'report_name': 'checkM_result'
        }

        returnVal.update(reportVal)

        return returnVal





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

        return self.package_folder(crit_out_dir, 'selected_output.zip', 'Selected output files from the CheckM analysis.')



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



    def build_html_output(self, plots_folder, output_folder, object_name):
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
        input_dir = dsu.stage_input(params['input_ref'], 'fna')
        output_dir = os.path.join(self.scratch, 'output_' + os.path.basename(input_dir['input_dir']))
        plots_dir = os.path.join(self.scratch, 'plot_' + os.path.basename(input_dir['input_dir']))
        log('Staged input directory: ' + input_dir['input_dir'])


        # 2) run the lineage workflow
        checkM_params = {'bin_folder': input_dir['input_dir'],
                         'out_folder': output_dir,
                         'checkM_cmd_name': 'lineage_wf',
                         'thread': 2,
                         'reduced_tree': 1
                         }
        lineage_wf_cmd = self._generate_command(checkM_params)
        self._run_command(lineage_wf_cmd)


        # 3) build the plots
        checkM_plot_params = {'bin_folder': input_dir['input_dir'],
                              'out_folder': output_dir,
                              'plots_folder': plots_dir,
                              'checkM_cmd_name': 'bin_qa_plot'
                              }
        bin_qa_plot_cmd = self._generate_command(checkM_plot_params)
        self._run_command(bin_qa_plot_cmd)


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

