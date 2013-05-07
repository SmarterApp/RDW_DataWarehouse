from distutils.core import setup
import subprocess

subprocess.call('cd ./scripts/; ./install_udl_requirements.sh', shell=True)

requires=['celery(>=3.0.19)']

scripts=['scripts/initialize_udl_database.sh',
         'scripts/start_rabbitmq.sh',
         'scripts/start_udl.sh',
         'scripts/initialize_udl_database.py',
         'scripts/start_rabbitmq.py',
         'scripts/start_udl.py']

setup(name='udl2', 
      version='0.1',
      description="Edware's Universal Data Loader",
      author="Amplify Insight Edware Team",
      author_email="edwaredev@wgen.net",
      package_dir={'udl2':'src/udl2'},
      packages=['udl2'],
      url='https://github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0/',
      scripts=scripts,
      requires=requires
) 
