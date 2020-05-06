import unittest, setup

from unittest.mock import patch, Mock
from datetime import date

from commands.trends_command import *
from commands.botcommand import BotCommand
from botquery import BotQuery
from boterror import BotError

class TrendsCommandTest(unittest.TestCase):
    def test_get_country_key(self):
        self.assertEqual(get_country_key("canada"), "canada")
        self.assertEqual(get_country_key("usa"), "united_states")
        self.assertEqual(get_country_key("UNITED STATES "), "united_states")
        self.assertEqual(get_country_key(" uS "), "united_states")
        self.assertEqual(get_country_key("     states "), "united_states")
        self.assertEqual(get_country_key("New ZEALAND"), "new zealand")
        self.assertEqual(get_country_key("Burkina FAso"), "burkina_faso")

    def test_get_initial_date_good(self):
        self.assertEqual(get_initial_date(date(2020, 4, 5), "1d"), date(2020, 4, 4))
        self.assertEqual(get_initial_date(date(2020, 1, 1), "1d"), date(2019, 12, 31))
        self.assertEqual(get_initial_date(date(2018, 7, 26), "5d"), date(2018, 7, 21))
        self.assertEqual(get_initial_date(date(2020, 4, 5), "1d"), date(2020, 4, 4))

        self.assertEqual(get_initial_date(date(2020, 10, 30), "2w"), date(2020, 10, 16))
        self.assertEqual(get_initial_date(date(2020, 1, 10), "4w"), date(2019, 12, 13))
        self.assertEqual(get_initial_date(date(2020, 3, 5), "1w"), date(2020, 2, 27))
        self.assertEqual(get_initial_date(date(2019, 3, 5), "1w"), date(2019, 2, 26))

        self.assertEqual(get_initial_date(date(2017, 9, 30), "1m"), date(2017, 8, 31))
        self.assertEqual(get_initial_date(date(2016, 5, 31), "1m"), date(2016, 5, 1))
        self.assertEqual(get_initial_date(date(2015, 5, 31), "2m"), date(2015, 4, 1))

        self.assertEqual(get_initial_date(date(2010, 1, 1), "1y"), date(2009, 1, 1))
        self.assertEqual(get_initial_date(date(2013, 12, 31), "3y"), date(2011, 1, 1))

        self.assertEqual(get_initial_date(date(2012, 6, 5), "0d"), date(2012, 6, 5))
        self.assertEqual(get_initial_date(date(2012, 6, 5), "0w"), date(2012, 6, 5))
        self.assertEqual(get_initial_date(date(2012, 6, 5), "0m"), date(2012, 6, 5))
        self.assertEqual(get_initial_date(date(2012, 6, 5), "0y"), date(2012, 6, 5))
        
    def test_validate_year_str_good(self):
        validate_year_str("2020")
        validate_year_str("2019")
        validate_year_str("1978")
        validate_year_str("100")
    
    def test_validate_year_str_bad(self):
        self.assertRaises(BotError, validate_year_str, "0")
        self.assertRaises(BotError, validate_year_str, "-2020")
        self.assertRaises(BotError, validate_year_str, "year")
        self.assertRaises(BotError, validate_year_str, "2017b")
        self.assertRaises(BotError, validate_year_str, "-100")
        self.assertRaises(BotError, validate_year_str, "")
        
    def test_trending_default(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "trending"])
        with patch("commands.trends_command.TrendsCommand.execute_trending_searches") as mock_execute_trending_searches:
            trends_command.execute()
            mock_execute_trending_searches.assert_called_once_with("united_states")
    
    def test_trending_location_1(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "trending", "MEXICO"])
        with patch("commands.trends_command.TrendsCommand.execute_trending_searches") as mock_execute_trending_searches:
            trends_command.execute()
            mock_execute_trending_searches.assert_called_once_with("mexico")
    
    def test_trending_location_2(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "trenDing", "South Korea"])
        with patch("commands.trends_command.TrendsCommand.execute_trending_searches") as mock_execute_trending_searches:
            trends_command.execute()
            mock_execute_trending_searches.assert_called_once_with("south_korea")

    @patch('commands.trends_command.date', Mock(today=lambda: date(2016, 7, 8)))
    def test_top_default_year(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "TOp"])
        with patch("commands.trends_command.TrendsCommand.execute_top_searches") as mock_execute_top_searches:
            trends_command.execute()
            mock_execute_top_searches.assert_called_once_with("2015")

    @patch('commands.trends_command.date', Mock(today=lambda: date(2020, 2, 6)))
    def test_top_given_year(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "tOp", "2011"])
        with patch("commands.trends_command.TrendsCommand.execute_top_searches") as mock_execute_top_searches:
            trends_command.execute()
            mock_execute_top_searches.assert_called_once_with("2011")

    @patch("commands.trends_command.TrendsCommand.get_help_text")
    def test_get_help_text(self, mock_get_help_text):
        mock_get_help_text.return_value = "halp"
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "help", "other", "useless", "arg"])
        with patch("commands.trends_command.TrendsCommand.handle_normal_query") as mock_handle_normal_query:
            trends_command.execute()
            mock_handle_normal_query.assert_called_once_with("halp")
    
    def test_graph_good_default(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graPH", "subject1", "subject2"])
        with patch("commands.trends_command.TrendsCommand.execute_graph") as mock_execute_graph:
            trends_command.execute()
            mock_execute_graph.assert_called_once_with({
                "keywords": ["subject1", "subject2"]
            })

    def test_graph_good_time_long(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graPH", "--time", "4w", "subject1", "subject2"])
        with patch("commands.trends_command.TrendsCommand.execute_graph") as mock_execute_graph:
            trends_command.execute()
            mock_execute_graph.assert_called_once_with({
                "keywords": ["subject1", "subject2"],
                "--time": "4w"
            })

    def test_graph_good_time_short(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graph", "-t", "12d", "subject1", "subject2"])
        with patch("commands.trends_command.TrendsCommand.execute_graph") as mock_execute_graph:
            trends_command.execute()
            mock_execute_graph.assert_called_once_with({
                "keywords": ["subject1", "subject2"],
                "--time": "12d"
            })

    def test_graph_good_time_long_different_order(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graph", "subject1", "subject2", "subject3", "--time", "1y"])
        with patch("commands.trends_command.TrendsCommand.execute_graph") as mock_execute_graph:
            trends_command.execute()
            mock_execute_graph.assert_called_once_with({
                "keywords": ["subject1", "subject2", "subject3"],
                "--time": "1y"
            })

    def test_graph_good_time_short_different_order(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graph", "subject1", "-t", "7d", "subject2", "test"])
        with patch("commands.trends_command.TrendsCommand.execute_graph") as mock_execute_graph:
            trends_command.execute()
            mock_execute_graph.assert_called_once_with({
                "keywords": ["subject1", "subject2", "test"],
                "--time": "7d"
            })

    def test_graph_bad_no_time_argument(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graph", "github", "-t"])
        with patch("commands.trends_command.TrendsCommand.handle_normal_query") as mock_handle_normal_query:
            trends_command.execute()
            mock_handle_normal_query.assert_called_once_with("Unable to fetch the trends: No argument provided for option '-t'")

    def test_graph_bad_no_mode(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends"])
        with patch("commands.trends_command.TrendsCommand.handle_normal_query") as mock_handle_normal_query:
            trends_command.execute()
            mock_handle_normal_query.assert_called_once_with("Unable to fetch the trends: No mode provided. Use '/trends help' for more info")
        
    def test_graph_bad_unknown_mode(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "mymode"])
        with patch("commands.trends_command.TrendsCommand.handle_normal_query") as mock_handle_normal_query:
            trends_command.execute()
            mock_handle_normal_query.assert_called_once_with("Unable to fetch the trends: Unknown mode 'mymode'")
            
    def test_graph_bad_graph_no_keywords(self):
        query = BotQuery()
        trends_command = TrendsCommand(query, ["/trends", "graph"])
        with patch("commands.trends_command.TrendsCommand.handle_normal_query") as mock_handle_normal_query:
            trends_command.execute()
            mock_handle_normal_query.assert_called_once_with("Unable to fetch the trends: No keywords provided for graphing")
