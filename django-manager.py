import sys
import os
import shutil


CURRENT_PATH = os.getcwd()
PROJECT_NAME = CURRENT_PATH.split("/")[-1]

file_list = os.listdir(CURRENT_PATH)
app_list = []

for file_name in file_list:
    if file_name[0] != ".":
        if file_name != PROJECT_NAME:
            path_to_file = os.path.join(CURRENT_PATH, file_name)
            if os.path.isdir(path_to_file):
                app_list.append(path_to_file)


def resetmigrations():
    if_deleted = False
    for app_path in app_list:
        migrations_folder = os.path.join(app_path, "migrations")
        if os.path.exists(migrations_folder):
            files_in_migrations_folder = os.listdir(migrations_folder)
            for migration in files_in_migrations_folder:
                path_to_migration_file = os.path.join(migrations_folder, migration)
                if migration != "__init__.py":
                    if_deleted = True
                    if os.path.isdir(path_to_migration_file):
                        shutil.rmtree(path_to_migration_file)
                    else:
                        os.remove(path_to_migration_file)
    if if_deleted:
        print("Migrations cleanup completed")
    else:
        print("Do not have any migrations created.")


def checkisdjango():
    if "manage.py" not in file_list:
        print("not a valid django project")
        return False
    manage_file_path = os.path.join(CURRENT_PATH, "manage.py")
    manage_file = open(manage_file_path, "r")
    manage_file_txt = manage_file.read()

    if "DJANGO_SETTINGS_MODULE" not in manage_file_txt:
        print("not a valid django project")
        return False
    return True


def settingavailable(folder):
    if "settings.py" in os.listdir(folder):
        return True
    return False


def initmodels():
    for file in file_list:
        CURRENT_PATH_FILE = os.path.join(CURRENT_PATH, file)

        if os.path.isdir(CURRENT_PATH_FILE) and not settingavailable(CURRENT_PATH_FILE):
            MODEL_PATH = os.path.join(CURRENT_PATH_FILE, "models")
            MODEL_INIT_PATH = os.path.join(MODEL_PATH, "__init__.py")
            os.mkdir(MODEL_PATH)


def initviews():
    for file in file_list:
        CURRENT_PATH_FILE = os.path.join(CURRENT_PATH, file)

        if os.path.isdir(CURRENT_PATH_FILE) and not settingavailable(CURRENT_PATH_FILE):
            MODEL_PATH = os.path.join(CURRENT_PATH_FILE, "views")
            MODEL_INIT_PATH = os.path.join(MODEL_PATH, "__init__.py")
            os.mkdir(MODEL_PATH)


def createmodel(appname, modelname):
    APP_PATH = os.path.join(CURRENT_PATH, appname)
    MODELS_PATH = os.path.join(APP_PATH, "models")
    INIT_PATH = os.path.join(MODELS_PATH, "__init__.py")
    NEW_MODEL_PATH = os.path.join(MODELS_PATH, f"{modelname}.py")

    new_model = open(NEW_MODEL_PATH, "w")
    write_txt = f"from django.db import models\nimport uuid\n\n\nclass {modelname}(models.Model):\n\tid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)"
    new_model.write(write_txt)
    new_model.close()

    init_file = open(INIT_PATH, "a+")
    init_file.write(f"\nfrom .{modelname} import {modelname}")
    init_file.close()

    print(f"{modelname} created successfuly!")


def createview(appname, viewname):
    APP_PATH = os.path.join(CURRENT_PATH, appname)
    MODELS_PATH = os.path.join(APP_PATH, "views")
    INIT_PATH = os.path.join(MODELS_PATH, "__init__.py")
    NEW_MODEL_PATH = os.path.join(MODELS_PATH, f"{viewname}.py")

    new_model = open(NEW_MODEL_PATH, "w")
    write_txt = f"from rest_framework.views import APIView\nfrom rest_framework.response import Response\nfrom rest_framework import status\n\n\nclass {viewname}(APIView):\n\tdef get(self, request):\n\t\treturn Response('ok', status=status.HTTP_200_OK)"
    new_model.write(write_txt)
    new_model.close()

    init_file = open(INIT_PATH, "a+")
    init_file.write(f"\nfrom .{viewname} import {viewname}")
    init_file.close()

    print(f"{viewname} created successfuly!")


def createserializer(appname, serializername):
    APP_PATH = os.path.join(CURRENT_PATH, appname)
    MODELS_PATH = os.path.join(APP_PATH, "serializers")
    INIT_PATH = os.path.join(MODELS_PATH, "__init__.py")
    NEW_MODEL_PATH = os.path.join(MODELS_PATH, f"{serializername}.py")

    new_model = open(NEW_MODEL_PATH, "w")
    write_txt = f"from rest_framework import serializers\n\n\nclass {serializername}(serializers.ModelSerializer):\n\tclass Meta:\n\t\tmodel = 'ModelName'\n\t\tfields = []"
    new_model.write(write_txt)
    new_model.close()

    init_file = open(INIT_PATH, "a+")
    init_file.write(f"\nfrom .{serializername} import {serializername}")
    init_file.close()

    print(f"{serializername} created successfuly!")


def initFolder(folder_path, init_path):
    os.mkdir(folder_path)
    init = open(init_path, "w")
    init.close()


def initApp(app_path, yn):
    VIEWS_PATH = os.path.join(app_path, "views")
    MODELS_PATH = os.path.join(app_path, "models")
    SERIALIZERS_PATH = os.path.join(app_path, "serializers")
    TESTS_PATH = os.path.join(app_path, "tests")

    VIEWS_INIT_PATH = os.path.join(VIEWS_PATH, "__init__.py")
    MODELS_INIT_PATH = os.path.join(MODELS_PATH, "__init__.py")
    SERIALIZERS_INIT_PATH = os.path.join(SERIALIZERS_PATH, "__init__.py")
    TESTS_INIT_PATH = os.path.join(TESTS_PATH, "__init__.py")

    VIEWS_FILE = os.path.join(app_path, "views.py")
    MODELS_FILE = os.path.join(app_path, "models.py")
    SERIALIZERS_FILE = os.path.join(app_path, "serializers.py")
    TESTS_FILE = os.path.join(app_path, "tests.py")

    URL_FILES = os.path.join(app_path, "urls.py")

    if not os.path.exists(VIEWS_PATH):
        initFolder(VIEWS_PATH, VIEWS_INIT_PATH)

    if not os.path.exists(MODELS_PATH):
        initFolder(MODELS_PATH, MODELS_INIT_PATH)

    if not os.path.exists(SERIALIZERS_PATH):
        initFolder(SERIALIZERS_PATH, SERIALIZERS_INIT_PATH)

    if not os.path.exists(TESTS_PATH):
        initFolder(TESTS_PATH, TESTS_INIT_PATH)

    urls_files = open(URL_FILES, "w")
    urls_files.write(
        "from django.urls import path\nfrom . import views\n\nurlpatterns = [\n\n]"
    )
    urls_files.close()

    if yn == "y":
        if os.path.exists(VIEWS_FILE):
            os.remove(VIEWS_FILE)

        if os.path.exists(MODELS_FILE):
            os.remove(MODELS_FILE)

        if os.path.exists(SERIALIZERS_FILE):
            os.remove(SERIALIZERS_FILE)

        if os.path.exists(TESTS_FILE):
            os.remove(TESTS_FILE)


def initproject():
    print("Is that okay to delete views.py, models.py, serializers.py files? ")
    yn = input("(Content of the files will be delete) [y/n]: ")
    for file in file_list:
        CURRENT_PATH_FILE = os.path.join(CURRENT_PATH, file)

        if os.path.isdir(CURRENT_PATH_FILE) and not settingavailable(CURRENT_PATH_FILE):
            print(CURRENT_PATH_FILE)
            initApp(CURRENT_PATH_FILE, yn)


def startapp(appname):
    os.system(f"python manage.py startapp {appname}")
    APP_PATH = os.path.join(CURRENT_PATH, appname)
    initApp(APP_PATH, "y")
    print(f"App {appname} created successfully")


user_inputs = sys.argv[1:]

command1 = user_inputs[0] if len(user_inputs) > 0 else ""
command2 = user_inputs[1] if len(user_inputs) > 1 else ""
command3 = user_inputs[2] if len(user_inputs) > 2 else ""
command4 = user_inputs[3] if len(user_inputs) > 3 else ""
command5 = user_inputs[4] if len(user_inputs) > 4 else ""


if checkisdjango():
    if command1 == "help":
        print("initproject")
        print(
            "createmodel [app name] [model name] - model name should be 'TestModel' like this"
        )
        print(
            "createview [app name] [view name] - view name should be 'TestView' like this"
        )
        print(
            "createserializer [app name] [serializer name] - serializer name should be 'TestSerializer' like this"
        )
        print("resetmigrations")

    elif command1 == "initproject":
        initproject()

    elif command1 == "startapp":
        startapp(command2)

    elif command1 == "createmodel":
        command3 = f"{command3[0]}{command3[1:]}"
        createmodel(command2, command3)

    elif command1 == "createview":
        command3 = f"{command3[0]}{command3[1:]}"
        createview(command2, command3)

    elif command1 == "createserializer":
        command3 = f"{command3[0]}{command3[1:]}"
        createserializer(command2, command3)

    elif command1 == "resetmigrations":
        resetmigrations()

    else:
        print("Invalid command")
