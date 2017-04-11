# -*- coding: utf-8 -*-
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
    CHECKM_WORKFLOW_PATH = '/usr/local/bin/checkm'
    CHECKM_PROCACULATED_DATA_PATH = '/data/checkm_data/'

    def _validate_run_checkM_params(self, params):
        """
        _validate_run_checkM_params:
                validates params passed to run_checkM method
        """
        log('Start validating run_checkM params')

        # check for required parameters
        for p in ['checkM_command_name', 'putative_genomes_in_folder', 'putative_genomes_in_folder', 'workspace_name']:
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
        """

    def _gc_plot(self, bin_folder, plot_folder, dist_value):
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
        """

    def _coding_plot(self, out_folder, bin_folder, plot_folder, dist_value):
        """
        Create coding density (CD) histogram and delta-CD plot.

        Provides a plot analogous to the gc_plot suitable for assessing the coding density of
sequences within a genome bin

        Example: checkm coding_plot ./output ./bins ./plots 95
        """

    def _tetra_plot(self, out_folder, bin_folder, plot_folder, tetra_profile):
        """
        Create tetranucleotide distance (TD) histogram and delta-TD plot.

        Provides a plot analogous to the gc_plot suitable for assessing the tetranucleotide
signatures of sequences within a genome bin. The Manhattan distance is used for determine the
different between each sequences tetranucleotide signature and the tetranucleotide signature of
the entire genome bin. This plot requires a file indicating the tetranucleotide signature of all
sequences within the genome bins. This file can be creates with the ‘tetra’ command.

        Example: checkm tetra_plot ./output ./bins ./plots tetra.tsv 95
        """


    def _dist_plot(self, out_folder, bin_folder, plot_folder, tetra_profile, dist_value):
        """
        Create image with GC, CD, and TD distribution plots together.

        Produces a single figure combining the plots produced by gc_plot, coding_plot, and
tetra_plot. This plot requires a file indicating the tetranucleotide signature of all sequences within
the genome bins. This file can be creates with the ‘tetra’ command.

        Example: checkm dist_plot ./output ./bins ./plots tetra.tsv 95
        """


    def _nx_plot(self, bin_folder, plot_folder):
        """
        Create Nx-plots.

        Produces a plot indicating the Nx value of a genome bin for all values of x. This provides a
more comprehensive view of the quality of an assembly than simply considering N50.
        
        Example: checkm nx_plot ./bins ./plots
        """


    def _len_plot(self, bin_folder, plot_folder):
        """
        Cumulative sequence length plot.

        Produces a plot of the cumulative sequence length of a genome bin with sequences
organized from longest to smallest. This provides additional information regarding the quality of an
assembled genome.

        Example: checkm len_plot ./bins ./plots
        """


    def _len_hist(self, bin_folder, plot_folder):
        """
        Sequence length histogram.

        Produces a histogram of the number of sequences within a genome bin at different
sequence length intervals. This provides additional information regarding the quality of an
assembled genome.

        Example: checkm len_hist ./bins ./plots
        """


    def _marker_plot(self, out_folder, bin_folder, plot_folder):
        """
        Plot position of marker genes on sequences.

        Plots the position of marker genes on sequences within a genome bin. This provides
information regarding the extent to which marker genes are collocated. The number of marker
genes within a fixed size window (2.8 kbps in this example) is indicated by with different colours.
Sequences without any marker genes are not shown. 

        Example: checkm marker_plot ./output ./bins ./plots
        """


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


    def _cov_pca(self, bin_folder, plot_folder, coverage_file):
        """
        PCA plot of coverage profiles.

        Produces a principal component plot (PCA) of the coverage profile distance between
sequences within a putative genome. This plot requires a file indicating the coverage profile of all
sequences within the genome bins. This file can be creates with the ‘coverage’ command.

        Example: checkm cov_pca ./bins ./plots coverate.tsv
        """


    def _tetra_pca(self,  bin_folder, plot_folder, tetra_profile):
        """
        PCA plot of tetranucleotide signatures.

        Produces a principal component plot (PCA) indicating the tetranucleotide distance
between sequences within a putative genome. This plot requires a file indicating the tetranucleotide
signature of all sequences within the genome bins. This file can be creates with the ‘tetra’ command.

        Example: checkm tetra_pca ./bins ./plots tetra.tsv
        """



    def _generate_command(self, params):
        """
        _generate_command: generate checkm command
        """

        command = 'checkm '

        cmd_name = params.get('checkM_command_name')
        if (cmd_name):
            command += cmd_name

            """ The lineage_wf workflow command
                Example: checkm lineage_wf ./bins ./output
            """
            if(cmd_name == 'lineage_wf'):
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('out_folder'))

            """ The taxonomy_wf workflow command,
                Example: checkm taxonomy_wf domain Bacteria ./bins ./output
            """
            if(cmd_name == 'taxonomy_wf'):
                command += ' domain {}' . format(params.get('domain'))
                command += ' {}' . format(params.get('bin_folder'))
                command += ' {}' . format(params.get('out_folder'))

            if params.get('thread'):
                command += '-thread {} '.format(params.get('thread'))

        else:
            command = 'Invalid checkM command'

        log('Generated checmM command: {}'.format(command))

        return command

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


    def _stage_file(self, file):
        """
        _stage_file: download local file/ shock file to scratch area
        """

        log('Processing file: {}'.format(file))

        input_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(input_directory)

        if file.get('path'):
            # handle local file
            local_file_path = file['path']
            file_path = os.path.join(input_directory, os.path.basename(local_file_path))
            log('Moving file from {} to {}'.format(local_file_path, file_path))
            shutil.copy2(local_file_path, file_path)

        if file.get('shock_id'):
            # handle shock file
            log('Downloading file from SHOCK node: {}-{}'.format(self.shock_url,
                                                                 file['shock_id']))
            sys.stdout.flush()
            file_name = self.dfu.shock_to_file({'file_path': input_directory,
                                                'shock_id': file['shock_id']
                                                })['node_file_name']
            file_path = os.path.join(input_directory, file_name)

        sys.stdout.flush()
        file_path = self.dfu.unpack_file({'file_path': file_path})['file_path']

        return file_path

    def _stage_file_list(self, file_list):
        """
        _stage_file_list: download list of local file/ shock file to scratch area
                          and write result_file_path to file
        """

        log('Processing file list: {}'.format(file_list))

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        result_file = os.path.join(result_directory, 'result.txt')

        result_file_path = []

        if 'shock_id' in file_list:
            for file in file_list.get('shock_id'):
                file_path = self._stage_file({'shock_id': file})
                result_file_path.append(file_path)

        if 'path' in file_list:
            for file in file_list.get('path'):
                file_path = self._stage_file({'path': file})
                result_file_path.append(file_path)

        log('Saving file path(s) to: {}'.format(result_file))
        with open(result_file, 'w') as file_handler:
            for item in result_file_path:
                file_handler.write("{}\n".format(item))

        return result_file


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
        run_checkM: run the checkm commands

        required params:
        putative_genomes_in_folder: folder path that holds all putative genome files with (fna as the file extension) to be checkM-ed
        putative_genomes_out_folder: folder path that holds all the checkm workflow results 
        checkM_command_name: name of the CheckM command,e.g., lineage_wf or taxonomy_wf
        workspace_name: the name of the workspace it gets saved to.

        optional params:
        thread: number of threads; default 1
        external_genes: indicating an external gene call instead of using prodigal, default 0
        external_genes_file: the file containing genes for gene call, default "" 
        """
        log('--->\nrunning MaxBinUtil.run_maxbin\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_checkM_params(params)

        command = self._generate_command(params)

        existing_files = []
        for subdir, dirs, files in os.walk('./'):
            for file in files:
                existing_files.append(file)

        self._run_command(command)

        new_files = []
        for subdir, dirs, files in os.walk('./'):
            for file in files:
                if file not in existing_files:
                    new_files.append(file)
        
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

