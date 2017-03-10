#!/usr/bin/env python
#-*- coding: UTF-8 -*-


from __future__ import absolute_import
from behave.formatter.json import JSONFormatter

class HTMLFormatter(JSONFormatter):
    name = 'html'
    description = 'HTML dump of test run'

    def __init__(self, stream_opener, config):
        super(HTMLFormatter, self).__init__(stream_opener, config)


    def write_json_feature_separator(self):
        pass

    def write_json_header(self):
        self.stream.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="xmformat.css">
    <title>behave testing result</title>
</head>
<body>''')

    def write_json_footer(self):
        self.stream.write('''</body>
</html>''')

    def write_json_feature(self, feature_data):
        feature_class = None
        feature_text = feature_data['keyword'] + ": " + feature_data['name'] + "    @" + feature_data['location']
        if feature_data['status'] == "failed":
            feature_class = "label fail"
        elif feature_data['status'] == "passed":
            feature_class = "label pass"
        else:
            feature_class = "label pass"

        #feature_text = '<div class="%s">%s</div>' %(feature_classs, feature_text)
        self.stream.write('\t<div class="feature">\n')
        self.stream.write('\t<span class="{feature_class}">Feature:</span>\n'.format(feature_class=feature_class))
        self.stream.write('\t<span class="name">{feature_name}</span>\n'.format(feature_name=feature_data['name']))

        for scenario in feature_data['elements']:
            scenario_class = "label pass"
            for step in scenario['steps']:
                if step.has_key('result') and step['result']['status'] == "failed":
                    scenario_class = "label fail"
                    break
            #scenario_text = scenario['keyword'] + ": " + scenario['name'] + "    @" + scenario['location']
            #scenario_text = '<div class="%s">%s</div>' %(feature_class, scenario_text)
            self.stream.write('\t\t<div class="children scenario" style="display: block;">\n')
            self.stream.write('\t\t\t<span class="{scenario_class}">{keyword}</span>\n'.format(scenario_class=scenario_class,keyword=scenario['keyword']))
            self.stream.write('\t\t\t<span class="name">{name}</span>\n'.format(name=scenario['name']))
            for step in scenario['steps']:
                if step.has_key('result'):
                    if step['result']['status'] == "failed":
                        step_class = "label fail"
                        #step_text = step['keyword'] + " " + step['name'] + "    @" + step['match']['location']
                    else:
                        step_class = "label pass"
                        #step_text = step['keyword'] + " " + step['name'] + "    @" + step['match']['location']
                else:
                    step_class = "label skip"
                    #step_text = step['keyword'] + " " + step['name'] + "    @None"
                self.stream.write('\t\t\t<div class="children step" style="display: block;">\n')
                self.stream.write('\t\t\t\t<span class="{step_class}">step:</span>\n'.format(step_class=step_class))
                self.stream.write('\t\t\t\t<span class="name">{name}</span>\n'.format(name=step['name']))
                if step.has_key('result') and step['result']['status'] == "failed":
                    self.stream.write('\t\t\t\t<div class="children lable error">%s</div>\n' % (step['result']['error_message']))
                #    for message in step['result']['error_message']:
                #        self.stream.write('\t\t\t\t<div class="children lable error">%s</div>' %(message))
                self.stream.write('\t\t\t</div>\n')

            self.stream.write('\t\t</div>\n')
        self.stream.write('\t</div>\n')
        self.stream.flush()

