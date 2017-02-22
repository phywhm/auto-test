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
        feature_classs = None
        feature_text = feature_data['keyword'] + ": " + feature_data['name'] + "    @" + feature_data['location']
        if feature_data['status'] == "failed":
            feature_classs = "feature_fail"
        elif feature_data['status'] == "passed":
            feature_classs = "feature_success"
        else:
            feature_classs = "feature_success"

        feature_text = '<div class="%s">%s</div>' %(feature_classs, feature_text)
        self.stream.write(feature_text)
        for scenario in feature_data['elements']:
            feature_class = "scenario_success"
            for step in scenario['steps']:
                if step.has_key('result') and step['result']['status'] == "failed":
                    feature_class = "scenario_fail"
                    break
            feature_classs = "scenario_success"
            scenario_text = scenario['keyword'] + ": " + scenario['name'] + "    @" + scenario['location']
            scenario_text = '<div class="%s">%s</div>' %(feature_class, scenario_text)
            self.stream.write(scenario_text)
            for step in scenario['steps']:
                if step.has_key('result'):
                    if step['result']['status'] == "failed":
                        step_class = "step_fail"
                        step_text = step['keyword'] + " " + step['name'] + "    @" + step['match']['location']
                    else:
                        step_class = "step_success"
                        step_text = step['keyword'] + " " + step['name'] + "    @" + step['match']['location']
                else:
                    step_class = "step_skip"
                    step_text = step['keyword'] + " " + step['name'] + "    @None"
                step_text  = '<div class="%s">%s</div>' %(step_class, step_text)
                self.stream.write(step_text)
                if step.has_key('result') and step['result']['status'] == "failed":
                    for message in step['result']['error_message']:
                        step_text = '<div class="trace_log">%s</div>' %(message)
                        self.stream.write(step_text)
        self.stream.flush()

