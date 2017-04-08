# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json

from kb_Msuite.Utils.CheckMUtil import CheckMUtil
#END_HEADER


class kb_Msuite:
    '''
    Module Name:
    kb_Msuite

    Module Description:
    A KBase module: kb_Msuite
This SDK module is developed to wrap the open source package CheckM which consists of a set of tools 
for assessing the quality of genomes recovered from isolates, single cells, or metagenomes. 
CheckM consists of a series of commands in order to support a number of different analyses and workflows.

References: 
CheckM in github: http://ecogenomics.github.io/CheckM/
CheckM docs: https://github.com/Ecogenomics/CheckM/wiki

Parks DH, Imelfort M, Skennerton CT, Hugenholtz P, Tyson GW. 2015. CheckM: assessing the quality of microbial genomes recovered from isolates, single cells, and metagenomes. Genome Research, 25: 1043–1055.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/qzzhang/kb_Msuite"
    GIT_COMMIT_HASH = "425f4dc5423f7a6210d1d30738a09c59a5b015dd"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        #END_CONSTRUCTOR
        pass


    def run_checkM(self, ctx, params):
        """
        :param params: instance of type "CheckMInputParams" 
        
        required parameters in params:
           putative_genomes_folder: folder path that holds all putative
           genome files with (fna as the file extension) to be checkM-ed

           checkM_workflow_name: name of the CheckM workflow,e.g., lineage_wf
           or taxonomy_wf 
           
           file_extension: the extension of the putative genome file, should be "fna" 
           
           workspace_name: the name of the workspace it gets saved to.
        
        option params:           
           thread: number of threads; default 1 external_genes: indicating an
           external gene call instead of using prodigal, default 0
           external_genes_file: the file containing genes for gene call,default "" 
           markerset: choose between 107 marker genes by default or 40 marker genes
           plotmarker: specify this option if you want to plot the markers in each 
           
           https://github.com/Ecogenomics/CheckM/wiki/Installation#how-to-inst
           all-checkm) 
           
        :returns: instance of type "CheckMResults" 
           checkM_results_folder: folder path that stores the CheckM results 
           report_name: report name generated by KBaseReport 
           report_ref: report reference generated by KBaseReport
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_checkM
        print '--->\nRunning kb_Msuite.run_checkM\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        checkM_runner = CheckMUtil(self.config)
        returnVal = checkM_runner.run_checkM(params)
        #END run_checkM

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_checkM return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
