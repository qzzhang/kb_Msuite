# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from Workspace.WorkspaceClient import Workspace as workspaceService

from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from MetagenomeUtils.MetagenomeUtilsClient import MetagenomeUtils

from kb_Msuite.kb_MsuiteImpl import kb_Msuite
from kb_Msuite.kb_MsuiteServer import MethodContext
from kb_Msuite.authclient import KBaseAuth as _KBaseAuth
from kb_Msuite.Utils.CheckMUtil import CheckMUtil

class kb_MsuiteTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_Msuite'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_Msuite',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_Msuite(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.checkm_runner = CheckMUtil(cls.cfg)

        suffix = int(time.time() * 1000)
        wsName = "test_kb_Msuite_" + str(suffix)
        cls.ws_info = cls.wsClient.create_workspace({'workspace': wsName})
        cls.au = AssemblyUtil(os.environ['SDK_CALLBACK_URL'])
        cls.mu = MetagenomeUtils(os.environ['SDK_CALLBACK_URL'])

        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx


    def test_CheckMUtil_generate_command(self):
        input_params = {
            'bin_folder': 'my_bin_folder',
            'out_folder': 'my_out_folder',
            'checkM_cmd_name': 'lineage_wf'
        }
        #expect_command = '/kb/deployment/bin/CheckMBin/checkm ' + 'lineage_wf '
        expect_command = '/usr/local/bin/checkm ' + 'lineage_wf '
        expect_command += ' -t 2 '
        expect_command += 'my_bin_folder my_out_folder '
        #command = self.checkm_runner._generate_command(input_params)
        #self.assertEquals(command, expect_command)

    def test_CheckMUtil_run_command(self):
        bin_folder = "/data/checkm_data/test_data"
        out_folder = "./test_results"
        command = '/usr/local/bin/checkm' + ' lineage_wf' + ' -t 2 ' + bin_folder + " " + out_folder
        #self.checkm_runner._run_command(command)

    def test_CheckMUtil_lineage_wf(self):
        bin_folder = "/data/checkm_data/test_data"
        out_folder = "./test_results"
        #self.checkm_runner._lineage_wf(bin_folder, out_folder, 2)


    def test_CheckMUtil_bin_qa_plot(self):
        bin_folder = "/data/checkm_data/test_data"
        out_folder = "./test_results"
        plot_folder = "./qa_plots"
        #self.checkm_runner._bin_qa_plot(out_folder, bin_folder, plot_folder)


    def test_CheckMUtil_run_checkM(self):
        bin_folder = "/data/checkm_data/test_data"
        out_folder = "./test_results"
        input_parameters = {
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'checkM_cmd_name': 'lineage_wf',
            'thread': 2
        }
        #self.checkm_runner.run_checkM(input_parameters)

    def test_run_checkM1(self):
        bin_folder = "/data/checkm_data/test_data"
        out_folder = "./test_results"
        input_params = {
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'checkM_cmd_name': 'lineage_wf',
            'workspace_name': self.getWsName(),
            'thread': 2
        }
        result = self.getImpl().run_checkM(self.getContext(), input_params)[0]

        self.assertTrue('checkM_results_folder' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)

    def test_run_checkM2(self):
        bin_folder = "/data/checkm_data/test_data"
        out_folder = "./test_results"
        plot_folder = "./qa_plot"
        input_params = {
            'bin_folder': bin_folder,
            'out_folder': out_folder,
            'plot_folder': plot_folder,
            'checkM_cmd_name': 'bin_qa_plot',
            'workspace_name': self.getWsName()
        }
        result = self.getImpl().run_checkM(self.getContext(), input_params)[0]

        self.assertTrue('checkM_results_folder' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)
