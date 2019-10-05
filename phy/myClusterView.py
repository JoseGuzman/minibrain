"""
myClusterView.py

Jose Guzman, jose.guzman<at>guzman-lab.com
created: Sat Oct  5 16:53:12 CEST 2019

A list of plugins to use hat contains custom statistics
for clusters in phy2. To use it add this file to 
~/.phy/plugings/ and modify ~/.phy/phy_config.py to 
contain the following line:
c.TemplateGUI.plugins = ['ISImedian']

"""
import numpy as np

from phy import IPlugin, connect
from phy.cluster import Clustering


class Test(IPlugin):
    def attach_to_controller(self, controller):
        """
        This function is called with the TemplateController
        instance as argument for every phy pluging. The TemplateController
        object gives you access to objects, data and views in the GUI.
        """
        @connect(sender = controller)
        def on_gui_ready(sender, gui):
            """
            Called when the GUI and all objects are fully loaded.
            It makes sure that controller.supervisor is properly defined.
            """
            @connect(sender = controller.supervisor)
            def on_cluster(sender, event):
                """
                Called every time a cluster assignment or cluster 
                group/label changes.
                """
                print("Clusters update: %s" % event)


class ISImedian(IPlugin):
    """
    This Pluging computes the median inter-spike interval of a cluster 
    """
    def attach_to_controller(self, controller):
        """
        This function is called at initialization time before
        creation of the supervisor object (s) which controls the 
        clusters and the similarity view.
        """
        
        def medianisi(cluster_id):
            """
            computes the median of the interstimulus interval
            of the cluster_id
            """
            t = controller.get_spike_times(cluster_id).data
            return np.median(np.diff(t)) if len(t)>2 else 0

        # will appear in ClusterView and SimilarityView
        controller.cluster_metrics['ISI.median'] = \
            controller.context.memcache(medianisi)
