import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
        sys.path.append(module_path)
from keys import *
import warnings
warnings.filterwarnings("ignore")

# if not on a windows machine, modify the HOME env variable
if os.name != 'nt':
    os.environ['HOME'] = '/research/iprobe-ashbau12'
os.environ['OPENAI_API_KEY'] = openai_api_key

from PIL import Image
from IPython.core.display import HTML
from functools import partial

from engine.utils import ProgramGenerator, ProgramInterpreter
from prompts.gqa import create_prompt
from prompts.knowtag import PROMPT


def setup(image_path, dataset):
    interpreter = ProgramInterpreter(dataset=dataset)
    prompter = partial(create_prompt,method='all')
    generator = ProgramGenerator(prompter=prompter)
    image = Image.open(image_path)
    image.thumbnail((640,640),Image.Resampling.LANCZOS)
    init_state = dict(
            IMAGE=image.convert('RGB')
    )
    image

    return generator, interpreter, init_state, image


def setup_ok_det(image_path, dataset):
    interpreter = ProgramInterpreter(dataset='okDet')
    def create_prompt(instruction):
            return PROMPT.format(instruction=instruction,list_max=20)

    generator = ProgramGenerator(prompter=create_prompt)
    image = Image.open(image_path)
    image.thumbnail((640,640),Image.ANTIALIAS)
    init_state = dict(
            IMAGE=image.convert('RGB')
    )
    return generator, interpreter, init_state, image


def run_gqa(prompt, generator, interpreter, init_state):
    program, _ = generator.generate(dict(question=prompt))
    result, prog_state = interpreter.execute(program, init_state, inspect=False)
    print('\n\n')
    print(30*'*')
    print(prompt)
    print(result)
    print(30*'*')
    return result


def ok_det_run(instruction, generator, interpreter, init_state):
    program, _ = generator.generate(instruction)
    result, prog_state = interpreter.execute(program, init_state, inspect=False)
    print('\n\n')
    print(30*'*')
    print(instruction)
    print(result)
    print(30*'*')
    return result
