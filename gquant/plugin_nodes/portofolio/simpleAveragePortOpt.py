from gquant.dataframe_flow import Node
from gquant.dataframe_flow._port_type_node import _PortTypesMixin
from gquant.dataframe_flow.portsSpecSchema import ConfSchema


class SimpleAveragePortOpt(Node, _PortTypesMixin):

    def init(self):
        _PortTypesMixin.init(self)
        self.INPUT_PORT_NAME = 'stock_in'
        self.OUTPUT_PORT_NAME = 'stock_out'
        cols_required = {"datetime": "date",
                         "strategy_returns": "float64",
                         "asset": "int64"}
        self.required = {
            self.INPUT_PORT_NAME: cols_required
        }

    def columns_setup(self):
        retention = {"datetime": "date",
                     "strategy_returns": "float64"}
        return _PortTypesMixin.retention_columns_setup(self,
                                                       retention)

    def ports_setup(self):
        return _PortTypesMixin.ports_setup(self)

    def conf_schema(self):
        json = {
            "title": "Simple Portfolio Node configure",
            "type": "object",
            "description": """Average the strategy returns for all the
            assets """,
        }
        ui = {
        }
        return ConfSchema(json=json, ui=ui)

    def process(self, inputs):
        """
        Average the strategy returns for all the assets.

        Arguments
        -------
         inputs: list
            list of input dataframes.
        Returns
        -------
        dataframe
        """
        input_df = inputs[self.INPUT_PORT_NAME]
        port = input_df[['datetime', 'strategy_returns']] \
            .groupby(['datetime']).mean().reset_index()
        port.columns = ['datetime', 'strategy_returns']
        return {self.OUTPUT_PORT_NAME: port}
