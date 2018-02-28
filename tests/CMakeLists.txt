# Test if mongod is present for tests that require it.
find_program(MONGOD_EXECUTABLE mongod)
if("${MONGOD_EXECUTABLE}" STREQUAL "MONGOD_EXECUTABLE-NOTFOUND")
  set(MONGOD_EXECUTABLE "local mongod required")
endif()

# Test if mongos is present for tests that require it.
find_program(MONGOS_EXECUTABLE mongod)
if("${MONGOS_EXECUTABLE}" STREQUAL "MONGOS_EXECUTABLE-NOTFOUND")
  set(MONGOS_EXECUTABLE "local mongos required")
endif()

python_tests_init()
javascript_tests_init()

if(RUN_CORE_TESTS)
  add_eslint_test(grunt_main Gruntfile.js)
  add_eslint_test(grunt_modules grunt_tasks)
  add_eslint_test(test_specs clients/web/test)
  add_eslint_test(swagger clients/web/static/girder-swagger.js)
  add_eslint_test(jquery_client clients/jquery)

  add_python_style_test(python_static_analysis_core "${PROJECT_SOURCE_DIR}/girder")
  add_python_style_test(python_static_analysis_core_tests "${PROJECT_SOURCE_DIR}/tests")
  add_python_style_test(python_static_analysis_core_pytest_girder "${PROJECT_SOURCE_DIR}/pytest_girder")
  add_python_style_test(python_static_analysis_ansible_client_tests
    "${PROJECT_SOURCE_DIR}/devops/ansible/roles/girder/library")

  # These are performed approximately in the order listed.
  add_python_test(api_describe)
  add_python_test(assetstore)
  add_python_test(collection)
  add_python_test(file)
  add_python_test(filter_logging)
  add_python_test(folder)
  add_python_test(group)
  add_python_test(item)
  add_python_test(model_singleton)
  add_python_test(notification TIMEOUT 50)
  add_python_test(resource)
  add_python_test(rest_decorator BIND_SERVER)
  add_python_test(routes BIND_SERVER)
  add_python_test(search)
  add_python_test(setting)
  add_python_test(sftp)
  add_python_test(stream BIND_SERVER TIMEOUT 90)
  # The system test depends on javascript-generate version information, so add
  # it to the integration group.
  add_python_test(system)
  set_property(TEST server_system PROPERTY LABELS girder_integration)
  # Upload test uses mongo replicaset and a lot of resources, so we run it by itself
  add_python_test(upload RUN_SERIAL RESOURCE_LOCKS replicaset REQUIRED_FILES "${MONGOD_EXECUTABLE}" "${MONGOS_EXECUTABLE}")
  set_property(TEST server_upload PROPERTY LABELS girder_integration)
  add_python_test(user)
  add_python_test(setup_database)

  add_python_test(py_client.cli BIND_SERVER RESOURCE_LOCKS py_client_test_dir)
  add_python_test(py_client.lib BIND_SERVER RESOURCE_LOCKS py_client_test_dir)

  add_pytest_test(core)

  add_web_client_test(data_filesystem "${PROJECT_SOURCE_DIR}/clients/web/test/spec/dataSpec.js" ASSETSTORE filesystem)
  add_web_client_test(data_gridfs "${PROJECT_SOURCE_DIR}/clients/web/test/spec/dataSpec.js" ASSETSTORE gridfs)
  add_web_client_test(data_gridfsrs "${PROJECT_SOURCE_DIR}/clients/web/test/spec/dataSpec.js" ASSETSTORE gridfsrs RESOURCE_LOCKS replicaset REQUIRED_FILES "${MONGOD_EXECUTABLE}")
  if (BUILD_JAVASCRIPT_TESTS)
    set_property(TEST web_client_data_gridfsrs PROPERTY LABELS girder_integration)
  endif()
  add_web_client_test(data_gridfsshard "${PROJECT_SOURCE_DIR}/clients/web/test/spec/dataSpec.js" ASSETSTORE gridfsshard RESOURCE_LOCKS replicaset REQUIRED_FILES "${MONGOD_EXECUTABLE}" "${MONGOS_EXECUTABLE}")
  if (BUILD_JAVASCRIPT_TESTS)
    set_property(TEST web_client_data_gridfsshard PROPERTY LABELS girder_integration)
  endif()
  add_web_client_test(data_s3 "${PROJECT_SOURCE_DIR}/clients/web/test/spec/dataSpec.js" ASSETSTORE s3 WEBSECURITY false)
  add_web_client_test(admin "${PROJECT_SOURCE_DIR}/clients/web/test/spec/adminSpec.js" ASSETSTORE s3 WEBSECURITY false
    PLUGIN_DIR "${PROJECT_SOURCE_DIR}/tests/test_plugins"
    ENABLEDPLUGINS "bad_server"
    RESOURCE_LOCKS replicaset
    )
  add_web_client_test(collection "${PROJECT_SOURCE_DIR}/clients/web/test/spec/collectionSpec.js")
  add_web_client_test(collection_base_class "${PROJECT_SOURCE_DIR}/clients/web/test/spec/collectionBaseClassSpec.js")
  add_web_client_test(model "${PROJECT_SOURCE_DIR}/clients/web/test/spec/modelSpec.js")
  add_web_client_test(group "${PROJECT_SOURCE_DIR}/clients/web/test/spec/groupSpec.js")
  add_web_client_test(user "${PROJECT_SOURCE_DIR}/clients/web/test/spec/userSpec.js")
  add_web_client_test(item "${PROJECT_SOURCE_DIR}/clients/web/test/spec/itemSpec.js")
  add_web_client_test(folder "${PROJECT_SOURCE_DIR}/clients/web/test/spec/folderSpec.js")
  add_web_client_test(routing "${PROJECT_SOURCE_DIR}/clients/web/test/spec/routingSpec.js")
  add_web_client_test(version "${PROJECT_SOURCE_DIR}/clients/web/test/spec/versionSpec.js")
  add_web_client_test(custom_widgets "${PROJECT_SOURCE_DIR}/clients/web/test/spec/customWidgetsSpec.js")
  add_web_client_test(widgets "${PROJECT_SOURCE_DIR}/clients/web/test/spec/widgetsSpec.js")
  add_web_client_test(datetime_widget "${PROJECT_SOURCE_DIR}/clients/web/test/spec/dateTimeWidgetSpec.js")
  add_web_client_test(sort_widget "${PROJECT_SOURCE_DIR}/clients/web/test/spec/sortWidgetSpec.js")
  add_web_client_test(empty_layout "${PROJECT_SOURCE_DIR}/clients/web/test/spec/emptyLayoutSpec.js")
  add_web_client_test(swagger "${PROJECT_SOURCE_DIR}/clients/web/test/spec/swaggerSpec.js" BASEURL "/api/v1")
  add_web_client_test(browser "${PROJECT_SOURCE_DIR}/clients/web/test/spec/browserSpec.js")
  add_web_client_test(set_api "${PROJECT_SOURCE_DIR}/clients/web/test/spec/setApiSpec.js")
  add_web_client_test(utilities "${PROJECT_SOURCE_DIR}/clients/web/test/spec/utilitiesSpec.js")

  # Add tests for the local TestData module
  add_plugin_data_path("has_external_data" "${PROJECT_SOURCE_DIR}/tests/test_plugins/has_external_data")
  add_python_test(external_data_core
    EXTERNAL_DATA "test_file.txt"
  )
  add_python_test(external_data_plugin
    EXTERNAL_DATA "plugins/has_external_data/plugin_test_file.txt"
  )
  set_property(TEST server_external_data_core PROPERTY LABELS girder_integration)
  set_property(TEST server_external_data_plugin PROPERTY LABELS girder_integration)

  add_subdirectory(clients)
  include(DocumentationTests.cmake)
endif()
