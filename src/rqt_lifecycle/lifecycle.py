# Copyright (c) 2024 Karl Damkjær Hansen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from rqt_gui_py.plugin import Plugin
from rqt_gui.ros2_plugin_context import Ros2PluginContext
# from python_qt_binding.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from ros2lifecycle.api import get_node_names, call_get_states, call_get_available_transitions
from ros2node.api import NodeName
# from ament_index_python.packages import get_package_share_directory
# from ros2node.api import get_absolute_node_name


class LifecycleTreeItem(QTreeWidgetItem):
    def __init__(self, node_name: NodeName, rqt_node):
        super(LifecycleTreeItem, self).__init__()
        self._node_name = node_name
        self.setText(0, node_name.full_name)

        states = call_get_states(node=rqt_node, node_names=[node_name.name])
        self.setText(1, states[node_name.name].label)

        transitions = call_get_available_transitions(node=rqt_node, states=states)
        transitions = transitions[node_name.name]
        t_str = ''
        for t in transitions:
            t_str = t_str + t.transition.label + ' | '
        t_str = t_str[:-3]
        self.setText(2, t_str)


class LifecycleMonitor(Plugin):

    def __init__(self, context: Ros2PluginContext):
        super(LifecycleMonitor, self).__init__(context)

        self.setObjectName('LifecycleMonitor')

        self._node = context.node

        self._widget = QWidget()
        self._widget.setWindowTitle('Lifecycle Monitor')
        # needed to update window title, kind of a bug, could be any string.
        self._widget.setObjectName('Lifecycle Monitor')

        self._widget.setLayout(QVBoxLayout())

        buttons_row = QWidget()
        buttons_row.setLayout(QHBoxLayout())
        configure_button = QPushButton('Configure')
        buttons_row.layout().addWidget(configure_button)
        cleanup_button = QPushButton('Clean up')
        buttons_row.layout().addWidget(cleanup_button)
        activate_button = QPushButton('Activate')
        buttons_row.layout().addWidget(activate_button)
        deactivate_button = QPushButton('Deactivate')
        buttons_row.layout().addWidget(deactivate_button)
        shutdown_button = QPushButton('Shut down')
        buttons_row.layout().addWidget(shutdown_button)
        self._widget.layout().addWidget(buttons_row)

        tree_widget = QTreeWidget()
        tree_widget.setColumnCount(3)
        tree_widget.setColumnWidth(0, 200)
        tree_widget.setColumnWidth(1, 150)
        tree_widget.setHeaderLabels(['Node', 'State', 'Transitions'])
        tree_widget.itemSelectionChanged.connect(self.on_item_selection_changed)
        self._widget.layout().addWidget(tree_widget)

        node_names = get_node_names(node=self._node, include_hidden_nodes=True)
        for n in node_names:
            node_item = LifecycleTreeItem(n, self._node)
            tree_widget.addTopLevelItem(node_item)

        context.add_widget(self._widget)

    def on_item_selection_changed(self):
        selected_items = self.sender().selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            print(f'Selected item: {selected_item.text(0)}')
