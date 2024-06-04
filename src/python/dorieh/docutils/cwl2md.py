#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Authors: Michael Bouzinier, Eugene Pokidov
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import argparse
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from dorieh.docutils.md_creator import MDCreator


cwl_src_content_template = """# CWL sub-workflow for step <u>*{step}*</u> of workflow {workflow}

```{{code-block}} yaml
:caption: CWL Content 
:linenos:

"""

cwl_src_template = """---
orphan: true
---

# {name}

```{literalinclude} ../../src/cwl/{path}
:linenos:
:language: yaml
```

"""



logger = logging.getLogger('script')
logger.addHandler(logging.StreamHandler())

arg_parser = argparse.ArgumentParser(description='Convert CWL files into Markdown')
arg_parser.add_argument(
    '-i', '--input-dir', type=str, required=True, dest='input_dir',
    help='An input directory with CWL files or path to a single CWL file'
)
arg_parser.add_argument(
    '-o', '--output-dir', type=str, required=True, dest='output_dir',
    help='The output dir for Markdown files'
)
arg_parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='An extended logging')


class CWLParser:
    def __init__(self, input_file_path: str, output_file_path: str, image_file_path: str, root=None):
        logger.info(output_file_path)
        self.input_file_path = input_file_path
        if root is None:
            self.root = self._get_filename(self.input_file_path)
        else:
            self.root = root

        with open(input_file_path, 'r') as cwl_file:
            self.raw_content = cwl_file.read()

        self.yaml_content = yaml.safe_load(self.raw_content)
        self.output_file_path = output_file_path
        self.image_file_path = image_file_path

        self.md_file = MDCreator(file_name=self.output_file_path)
        self.sub_workflow_counter = 0

    def parse(self, content: Dict = None, name=None):
        self._add_title()
        if content:
            self._add_source_content(content, name)
        else:
            self._add_source()
        self._add_image()
        self._add_contents()
        self._add_header()
        self._add_docs()
        self._add_inputs()
        self._add_outputs()
        self._add_steps()

        self.md_file.save()

    def _add_title(self):
        title = self._find_title(self.raw_content) or self._get_filename(self.output_file_path.replace('.md', '.cwl'))
        self.md_file.add_header(text=title, level=1)

    def _add_source(self):
        of = self.output_file_path.replace(".md", "cwl_src.md")
        inf = os.path.basename(self.input_file_path)
        content = cwl_src_template.format(name=inf, path=inf,
                                          literalinclude="{literalinclude}")
        with open(of, "w") as out:
            out.write(content)
        self.md_file.add_text("\n [Source code]({}) \n".format(
            os.path.basename(of)
        ))

    def _add_source_content(self, content: Dict, name):
        of = self.output_file_path.replace(".md", "cwl_src.md")

        with open(of, "w") as out:
            out.write(cwl_src_content_template.format(workflow=self.root, step=name))
            yaml.safe_dump(content, out)
            print("```", file=out)
        self.md_file.add_text("\n [Source code]({}) \n".format(
            os.path.basename(of)
        ))

    @staticmethod
    def _find_title(content: str) -> Optional[str]:
        for line in content.splitlines():
            if line.startswith('###'):
                return line.replace('###', '').strip()

    @staticmethod
    def _get_filename(file_path: str) -> str:
        return os.path.split(file_path)[1]

    def _add_contents(self):
        contents = [
            '```{contents}',
            '---',
            'local:',
            '---',
            '```',
        ]

        self.md_file.add_text('\n'.join(contents))

    def _add_image(self):
        if 'workflow' not in self.yaml_content['class'].lower():
            return

        subprocess.run(
            f'cwl-runner --print-dot {self.input_file_path} | dot -Tpng > {self.image_file_path}', shell=True
        )
        filename = self.image_file_path.split(os.path.sep)[-1]
        self.md_file.add_image(filename)

    def _add_header(self):
        if "expressiontool" in self.yaml_content['class'].lower():
            header = '**JavaScript Tool** '
        elif 'tool' in self.yaml_content['class'].lower():
            header = '**Tool**. Runs: ' + self._extract_tool(str(self.yaml_content['baseCommand']))
        elif 'workflow' in self.yaml_content['class'].lower():
            header = '**Workflow**'
        else:
            header = '**Unknown class**'

        self.md_file.add_text(header)

    def _extract_tool(self, base_command: str) -> str:
        tool = base_command.replace('[', '').replace(']', '').replace("'", '').split(', ')[-1]
        pp = tool.split('.')
        docpath = os.path.join("..", "members")
        if pp[0] == "dorieh":
            doc = os.path.join(docpath, pp[-1])
        else:
            return tool

        return f'[{tool}]({doc})'

    def _add_docs(self):
        if 'doc' not in self.yaml_content:
            return

        self.md_file.add_header(text='Description', level=2)
        self.md_file.add_text(self.yaml_content['doc'])

    def _add_inputs(self):
        self.md_file.add_header(text='Inputs', level=2)

        data = [('Name', 'Type', 'Default', 'Description')]
        for name, arg in self.yaml_content['inputs'].items():
            doc = tp = df = ''

            if isinstance(arg, str):
                doc = name
                tp = arg.replace('?', '')
                df = None
            elif isinstance(arg, dict):
                doc = arg.get('doc', ' ').replace('\n', ' ')
                tp = arg.get('type', 'string')
                df = arg.get('default', None)

            df = f'`{df}`' if df else ' '

            data.append((name, tp, df, doc))

        self.md_file.add_table(data=data)

    def _add_outputs(self):
        self.md_file.add_header(text='Outputs', level=2)

        data = [('Name', 'Type', 'Description')]
        for name, arg in self.yaml_content['outputs'].items():
            doc = arg.get('doc', ' ').replace('\n', ' ')
            tp = arg.get('type', 'string')

            if isinstance(tp, str):
                tp = tp.replace('?', '')
            elif isinstance(tp, dict):
                tp = tp['type']

            data.append((name, tp, doc))

        self.md_file.add_table(data=data)

    def _add_steps(self):
        if 'steps' not in self.yaml_content:
            return

        self.md_file.add_header(text='Steps', level=2)

        data = [('Name', 'Runs', 'Description')]
        for item in self.yaml_content['steps']:
            if isinstance(item, dict):
                name = item['id']
                arg = item
            else:
                name = item
                arg = self.yaml_content['steps'][name]

            doc = arg.get('doc', ' ').replace('\n', ' ')
            runs = arg['run']
            if isinstance(runs, str):
                ref_uri = runs.replace('.cwl', '.md')
                target = f'[{runs}]({ref_uri})'
            elif runs.get('class').lower() == 'workflow':
                file_name = self._handle_sub_workflow(name, runs)
                target = f"[sub-workflow]({file_name})"
            elif runs.get('class').lower() == 'expressiontool':
                target = "Evaluates JavaScript expression"
            else:
                target = runs.get('baseCommand', 'command')

            data.append((name, target, doc))

        self.md_file.add_table(data=data)

    def _handle_sub_workflow(self, step_name: str, data: Dict[str, Any]) -> str:
        prepared_data = {
            **data,
            'cwlVersion': self.yaml_content['cwlVersion'],
            'requirements': self.yaml_content['requirements'],
        }
        pipeline_file_name = self._get_filename(self.input_file_path)
        header = f'### Sub-workflow *{step_name}* from {pipeline_file_name} \n\n'

        source_dir, basename = os.path.split(self.input_file_path)

        with tempfile.NamedTemporaryFile(mode='w+', dir=source_dir, suffix=basename) as temp_file:
            temp_file.write(header)
            yaml.safe_dump(prepared_data, temp_file)

            self.sub_workflow_counter += 1
            output_file_path = self.output_file_path.replace('.md', f'_{self.sub_workflow_counter}.md')
            image_file_path = self.output_file_path.replace('.md', f'_{self.sub_workflow_counter}.png')

            CWLParser(
                temp_file.name,
                output_file_path,
                image_file_path,
                root=self.root
            ).parse(content=prepared_data, name=step_name)

            return self._get_filename(output_file_path)


def main():
    args = arg_parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)

    if os.path.isdir(args.input_dir):
        cwl_files = [
            os.path.join(os.path.abspath(args.input_dir), file_name)
            for file_name in os.listdir(args.input_dir)
        ]
    elif os.path.isfile(args.input_dir):
        cwl_files = [args.input_dir]
    else:
        raise ValueError("No such file or directory: " + args.input_dir)

    for input_file_path in cwl_files:
        if os.path.splitext(input_file_path)[1].lower() != '.cwl':
            continue

        file_name = os.path.basename(input_file_path)
        output_file_path = os.path.join(os.path.abspath(args.output_dir), file_name.replace('.cwl', '.md'))
        image_file_path = os.path.join(os.path.abspath(args.output_dir), file_name.replace('.cwl', '.png'))

        CWLParser(input_file_path, output_file_path, image_file_path).parse()


if __name__ == '__main__':
    main()
