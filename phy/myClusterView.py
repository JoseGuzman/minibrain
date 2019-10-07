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
from phy import emit
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
                group/label changes. It will print a message
                on the console where phy starts.
                """
                print("Clusters update: %s" % event)


class ISImedian(IPlugin):
    """
    This Pluging computes the median inter-spike interval of a cluster 
    """
    def attach_to_controller(self, controller):
        """
        This function is called at initialization time before
        creation of the supervisor object (s) which controls 
        ClusterView and SimilarityView.
        """
        
        def medianisi(cluster_id):
            """
            computes the median of the interstimulus interval
            of the cluster_id
            """
            t = controller.get_spike_times(cluster_id).data
            return np.median(np.diff(t)) if len(t)>2 else 0

        def cc_index(cluster_id):
            """
            computes the percentage of spikes within the
            refractory period.
            """
            pass

        # will appear in ClusterView and SimilarityView
        controller.cluster_metrics['ISI.median'] = \
            controller.context.memcache(medianisi)

class SpikeSplitter(IPlugin):
    """
    This Pluging select single spikes to be splitted 
    """
    def attach_to_controller(self, controller):
        """
        This function is called at initialization time before
        creation of the supervisor object (s) which controls  
        ClusterView and SimilarityView.
        """
        @connect(sender=controller)
        def on_gui_ready(sender, gui):
            """
            Called when the GUI and all objects are fully loaded.
            It makes sure that controller.supervisor is properly defined.
            """
            #------------------------------------------
            # File->Display message
            #------------------------------------------
            gui.file_actions.separator()
            @gui.file_actions.add()
            def show_selected_clusters():
                """
                Display selected clusters in the status bar
                """
                sel = controller.supervisor.selected
                gui.status_message = "Selected cluster/s: %s"%sel
            
            #------------------------------------------
            # in Select->MyPlugins:
            #------------------------------------------
            gui.select_actions.separator()
            myparams = dict(submenu='MyPlugins', shortcut = 'alt+p',
                prompt=True, prompt_default=lambda: 0)
            @gui.select_actions.add( **myparams )
            def split_spike(time):
                """
                split the spike next to the time entered
                """
                #@controller.supervisor.cluster_view.get_ids
                pspike = int(time * 30000)
                # get id from selected cluster
                mycluster_id = controller.supervisor.selected
                # get the sample of the first spike
                t = controller.get_spike_times(mycluster_id[0])
                p = controller.get_spike_ids(mycluster_id[0])
                x = np.argmax(t>time) 
                # remove this p[x]
                #emit('action', s.action_creator, 'split', list(p[x]))
                gui.status_message = 'Spike id: %s'%p[x]

        

            

