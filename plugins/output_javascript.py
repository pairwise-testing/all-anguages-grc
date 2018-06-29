#    This is part of grc module. Plugin provides export scenarios to python script
#    Copyright (C) 2018  Tomasz Otoka
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import Scenario

#---------- OBLIGATORY ------------
# extension = <file extension for plugin>
# type = <value> - please see 'Plugin.py'
extension = 'html'
type = 2 # output module
language = 'javascript'
#----------------------------------

output_path = 'Scenarios_%s' % language
output_prefix = 'Scenario_'


def run(parameters):
    stdOut = parameters['stdOut']
    scenarios = parameters['scenarios']

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for scenario in scenarios:

        scenario_file = open('%s/%s%s.%s' % (output_path, output_prefix, scenario.id, extension), 'w')

        for step in scenario.steps:

            if step.id == 0:

                scenario_file.write('<!DOCTYPE html>\n')
                scenario_file.write('<html>\n')
                scenario_file.write('<body>\n')
                scenario_file.write('<p>\n')

                scenario_file.write('This file was generated automatically<br>')
                scenario_file.write('Please do not edit this file - your changes will be lost after next file regeneration<br>')
                scenario_file.write('<br>Scenario:<br>')

                for descriptionStep in scenario.steps:
                    if descriptionStep.id > 0:
                        scenario_file.write('%s. %s<br>    ---> %s<br>' % (descriptionStep.id, descriptionStep.action.label, descriptionStep.node.label))

                scenario_file.write('</p>\n<p id="scenario"></p>\n')
                scenario_file.write('<script>\n')
                

            else:

                scenario_file.write('    document.getElementById("Scenario").innerHTML = "%s. %s ---> %s"<br>' % (step.id, step.action.label.replace('\n', ''), step.node.label.replace('\n', '')))
                for codeLine in step.action.code.split('\n'):
                    scenario_file.write('    %s\n' % codeLine)
                for nodeCodeLine in step.node.code.split('\n'):
                    scenario_file.write('    %s\n' % nodeCodeLine)

        scenario_file.write('</script>\n')
        scenario_file.write('</body>\n')
        scenario_file.write('</html>')

        scenario_file.close()

    stdOut.my_print('--- Scenarios saved to "%s"' % output_path)
