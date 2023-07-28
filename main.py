from Classes.GraphFunc import GraphFunc
import argparse
import os

#Only Output and GraphFunc Classes need to be customized to your needs.

#CMD argument parsing for filepath
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jsonpath", dest="jsonpath", default=os.path.dirname(os.path.abspath(__file__)) + "\\resources\\SkriptSettings_com.json", help="JsonPath:\tSpecifies which configuration file should be used. (Default: .\\O365Project\\resources\\SkriptSettings_com.json)", required=False)
parser.add_argument("-i","--IDList", dest="IDListStr", default="",help="IDList:\tThis Argument imports all MessageIds for updating to read", required=False)
#parser.add_argument("-c", "--Credentials", dest="credentials", default="", help="Credentials:\tThis Argument parses the Credentials in this format: TenantID@ClientID@ClientSecret")
#parser.add_argument("-e", "-Endpoint", default="", help="Endpoint:\t This Argument parses all Endpoint http addresses in this format: tokenEndpoint@GraphEndpoint@Authority")
#parser.add_argument("-s", "--Splitter", default="", help="Splitter:\t is uses to split Strings from cmdargs")
#parser.add_argument("-p", "--Proxy", default="", help="Proxy:\t this Argument parses the proxy Settings in this formats: ip@port,ip@port@username@password")
#parser.add_argument("-m", "--MailAddr", default="", help="MailAddr: This Argument parses the MailboxAddress in this format: example@comapny.com")
#parser.add_argument("-r", "--rights", default="", help="Rights:\tThis Argument parses select and scope in this format")
#parser.add_argument("-f", "--filter", default="", help="Filter:\tThis Argument parses the query in this format: ")
#parser.add_argument("-c", "-CreateJsonString", dest="jsonString", default="True" , help="CreateJsonString:\tThis Argument creates a JSONString and Outputs it", required=False)
args = parser.parse_args()
try:
    GraphFunc(args.jsonpath, args.IDListStr)
except:
    parser.print_help()

