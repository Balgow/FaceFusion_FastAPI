import sys
import subprocess

def swap_face(source_image, target_image, output_image) -> None:
	
	commands = [ sys.executable, 'run.py', 
			 '--frame-processors', 'face_swapper', 'face_enhancer', 
			 '--face-swapper-model', 'inswapper_128',
             '--face-enhancer-model', 'gfpgan_1.4',
			 '-s', '../images/'+source_image, '-t', '../images/'+target_image, '-o', '../images/'+output_image, '--headless' ]
	run = subprocess.run(commands, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, cwd='./facefusion')
	assert run.returncode == 0
	assert 'image succeed' in run.stdout.decode()
