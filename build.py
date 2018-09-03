from os import listdir, sys, path

project_path = path.dirname(path.abspath(__file__))
sys.path.append(f'{project_path}/main')

from pybuilder.core import use_plugin, init, Author, task, before
from pybuilder_demo import __version__

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin('pypi:pybuilder_pytest')
use_plugin('pypi:pybuilder_pytest_coverage')
use_plugin("copy_resources")
use_plugin("python.distutils")

name = "pybuilder-demo"
version = __version__
summary = "An example project for configuring pybuilder"
description = """An example project for configuring pybuilder."""

authors = [Author("Ravi Sharma", "ravi.sharma.cs11@gmail.com")]
url = "https://github.com/imravishar/pybuilder-conda"
license = "GPL License"
default_task = ["clean"]


@init
def initialize(project):
    project.set_property('dir_source_main_python', 'main')
    project.set_property('dir_source_pytest_python', 'unittest')
    project.set_property('dir_source_main_scripts', 'main/scripts')
    project.set_property("pytest_coverage_break_build_threshold", 90)
    project.set_property("pytest_coverage_html", True)


@before("run_unit_tests")
def configure_pytest(project):
    project.get_property("pytest_extra_args").append("-xsvv")
    project.get_property("pytest_extra_args").append("--junitxml=target/reports/junit.xml")


@before("package")
def package_configs_file(project, logger):
    logger.info("Copying non python source files i.e all config files")
    project.set_property('include_package_data', True)
    project.get_property("copy_resources_glob").append("environment.yml")
    project.get_property("copy_resources_glob").append("default_conf/*")
    project.set_property("copy_resources_target", "$dir_dist/pybuilder_demo")
    project.package_data.update({'pybuilder_demo': ["environment.yml", "default_conf/*"]})


@task(description="Setup configs files default location")
def package(project, logger):
    logger.info("All configs will be copied to 'anaconda<version>/envs/<conda-env>/etc' directory "
                "during installation")
    conf_source_directory = 'build/lib/pybuilder_demo/default_conf'
    dependencies_source_directory = "build/lib/pybuilder_demo"
    conf_destination = "etc/configs"
    dependencies_destination = "etc/.dependencies"
    config_files = map(lambda conf_file: "{0}/{1}".format(conf_source_directory, conf_file),
                       listdir(project.expand_path('$dir_dist/pybuilder_demo/default_conf')))

    dependencies_files = ["{0}/environment.yml".format(dependencies_source_directory)]
    project.files_to_install.extend([(conf_destination, config_files), (dependencies_destination, dependencies_files)])


@task(description="Run pybuilder-demo")
def run(project):
    from pybuilder_demo.main import start
    arg1 = project.get_property("arg1")
    arg2 = project.get_property("arg2")
    conf = project.get_property("conf")
    start(arg1, arg2, conf)
