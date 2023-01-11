var currentDeviceListObject = null; //global cache

function displayDeviceError(text)
{
    //set error message
    $("#error-device-div").html(text)

    //hide invalid elements
    $("#test-display-container").addClass("d-none")
    $("#test-version-error-container").addClass("d-none")
    $("#test-version-form-container").addClass("d-none")

    //show error message
    $("#test-device-error-container").removeClass("d-none")
}

function displayVersionError(text)
{
    //set error message
    $("#error-version-div").html(text)

    //hide invalid elements
    $("#test-display-container").addClass("d-none")

    //show error message
    $("#test-version-error-container").removeClass("d-none")
}

function hideErrors(device, version)
{
    if(device)
    {
        $("#test-device-form-container").addClass("d-none")
    }
    if(version)
    {
        $("#test-version-form-container").addClass("d-none")
    }
}

function hideErrors()
{
    hideErrors(true,true)
}

function createOption(value)
{
    var element = document.createElement("option");
    element.value = value;
    element.innerHTML = value;
    return element;
}

function findtestVersions()
{
    var versionList = []
    currentDeviceListObject.forEach(e => {
            versionList.push(e.device.version)
        }
    )
    
    var box = $("#device-version");
    box.empty()

    versionList.forEach(e =>
        {
            box.append(createOption(e))
        })
}

function displayTestList(version)
{
    if(currentDeviceListObject === null)
    {
        displayDeviceError("The device was never specified.")
    }

    var testList = null
    currentDeviceListObject.forEach(e => {
        if(e.device.version === version)
            {
                testList = e
            }
        }
    )

    if(testList === null)
    {
        displayVersionError("Software version couldn't be found")
        return;
    }
    
    $("#device-name-cell").find("h3").html(testList.device.name);
    $("#device-description").html(testList.device.description);
    $("#device-soft-ver").html(testList.device.version);
    
    $(".test-row").remove();

    testRowTemplate = $(".test-row-template").clone();
    testRowTemplate.removeClass("test-row-template");
    testRowTemplate.removeClass("d-none");
    testRowTemplate.addClass("test-row");

    testList.tests.forEach(element => {
        var row = testRowTemplate.clone();
        var name = element[0];
        var testResult = element[1];
        var testCaptureName = null
        if(element.length > 2)
        {
            testCaptureName = element[2]
        }

        row.find(".test-name-cell").html(name);
        row.find(".test-result-cell").html(testResult);

        potantial_vuln_tests = ["ping-frag-sep","ping I,E --amsdu"]
        //these test don't looks for vulnerabilities
        behavior_tests = ["ping", "ping I,E,E", "ping I,E,E --delay 1", "ping-frag-sep --pn-per-qos"]

        if(behavior_tests.indexOf(name) > -1)
        {
            if(testResult === "true")
            {
                row.find(".test-result-cell").html("Test Successful");
                row.addClass("table-success")
            }
            else if(testResult === "false")
            {
                row.find(".test-result-cell").html("Not supported");
                row.addClass("table-danger")
            }
            else
            {
                row.find(".test-result-cell").html("Result invalid or missing");
                row.addClass("table-warning")
            }
        }
        else if(potantial_vuln_tests.indexOf(name) > -1)
        {
            if(testResult === "true")
            {
                row.find(".test-result-cell").html("Potentially Vulnerable");
                row.addClass("table-warning")
            }
            else if(testResult === "false")
            {
                row.find(".test-result-cell").html("Secure");
                row.addClass("table-success")
            }
            else
            {
                row.find(".test-result-cell").html("Result invalid or missing");
                row.addClass("table-warning")
            }
        }
        else
        {
            if(testResult === "true")
            {
                row.find(".test-result-cell").html("Vulnerable");
                row.addClass("table-danger")
            }
            else if(testResult === "false")
            {
                row.find(".test-result-cell").html("Secure");
                row.addClass("table-success")
            }
            else
            {
                row.find(".test-result-cell").html("Result invalid or missing");
                row.addClass("table-warning")
            }
        }


        
        if(testCaptureName != null)
        {
            row.find(".test-download-link").attr("href", "/captures/" + testCaptureName);
        }
        else
        {
            row.find(".test-download-link").html("");
        }

        $("#device-test-table").append(row);
    });

    $("#test-display-container").removeClass("d-none");
}

function testListApiCallback(result, code)
{
    if(code === "success")
    {
        if(typeof result[Symbol.iterator] === 'function')
        {
            currentDeviceListObject = result
        }
        else
        {
            currentDeviceListObject = new Array()
            currentDeviceListObject.push(result);
        }
        findtestVersions()
        $("#test-version-form-container").removeClass("d-none")
    }
    else
    {
        displayDeviceError("Couldn't recieve device information. Code:" + code)
    }
}

function callTestListApi(deviceName)
{
    const apiurl = "/devices/";

    if(deviceName === "test_debug_device")
    {
        testJson = JSON.parse('[{"device":{"name":"Test Device","description":"Test Description","version":"1.23.486_test"},"tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]}]');
        testListApiCallback(testJson, "success");
    }
    else if(deviceName === "test_debug_device2")
    {
        testJson = JSON.parse('[{"device":{"name":"Test Device2","description":"Test Description","version":"1.23.486_test"},"tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]},\
        {"device":{"name":"Test Device2","description":"Test Description","version":"1.24.489_test"},"tests":[["testsucccess","false"],["testfail","false"],["testunknown","true"]]}]');
        testListApiCallback(testJson, "success");
    }
    else
    {
        $.ajax({
            url:apiurl+deviceName,
            dataType:"json",
            success:testListApiCallback
        })
    }
}

function submitTestSearch(event)
{
    event.preventDefault();

    //hide invalid containers
    $("#test-version-error-container").addClass("d-none")
    $("#test-display-container").addClass("d-none")

    var deviceVersion = $("#device-version").val();
    displayTestList(deviceVersion)
}

function submitDeviceTestSearch(event)
{
    event.preventDefault();

    //hide invalid containers
    $("#test-device-error-container").addClass("d-none")
    $("#test-version-form-container").addClass("d-none")
    $("#test-version-error-container").addClass("d-none")
    $("#test-display-container").addClass("d-none")

    var deviceName = $("#device-name").val();
    callTestListApi(deviceName);
}

function findDeviceAutocompleteListCallback(result, code)
{
    //result = JSON.stringify(result);
    if(code === "success")
    {
        try{
            deviceAutocompleteSet = Array.from(new Set(result.devices))
            $("#device-name").autocomplete(
                {
                    source:deviceAutocompleteSet
                }
              );
            $("#device-list-loading").addClass("d-none")
        }
        catch( error )
        {
            displayDeviceError("Couldn't parse the server response for autocomplete. " + error)
        }
    }
    else
    {
        displayDeviceError("Couldn't recieve device information for autocomplete. Code:" + code)
    }
}

function testListAllApiCallback(result, code)
{
    if(code === "success")
    {
    
        var testList = null
        // currentDeviceListObject.forEach(e => {
        //     if(e.device.version === version)
        //         {
        //             testList = e
        //         }
        //     }
        // )

        result.forEach(device =>
        {

            console.log(device)
            deviceName = device.device.name
            deviceVersion = device.device.version
            testList = device.tests

            //$(".test-row").remove();

            testRowTemplate = $(".test-row-template").clone();
            testRowTemplate.removeClass("test-row-template");
            testRowTemplate.removeClass("d-none");
            testRowTemplate.addClass("test-row");

            testList.forEach(element => {
                var row = testRowTemplate.clone();
                var testName = element[0];
                var testResult = element[1];
                var testCaptureName = null
                if(element.length > 2)
                {
                    testCaptureName = element[2]
                }

                row.find(".device-name-cell").html(deviceName);
                row.find(".device-version-cell").html(deviceVersion);
                row.find(".test-name-cell").html(testName);
                row.find(".test-result-cell").html(testResult);

                potantial_vuln_tests = ["ping-frag-sep","ping I,E --amsdu"]
                //these test don't looks for vulnerabilities
                behavior_tests = ["ping", "ping I,E,E", "ping I,E,E --delay 1", "ping-frag-sep --pn-per-qos"]

                if(behavior_tests.indexOf(testName) > -1)
                {
                    if(testResult === "true")
                    {
                        row.find(".test-result-cell").html("Test Successful");
                        row.addClass("table-success")
                    }
                    else if(testResult === "false")
                    {
                        row.find(".test-result-cell").html("Not supported");
                        row.addClass("table-danger")
                    }
                    else
                    {
                        row.find(".test-result-cell").html("Result invalid or missing");
                        row.addClass("table-warning")
                    }
                }
                if(potantial_vuln_tests.indexOf(testName) > -1)
                {
                    if(testResult === "true")
                    {
                        row.find(".test-result-cell").html("Potentially Vulnerable");
                        row.addClass("table-warning")
                    }
                    else if(testResult === "false")
                    {
                        row.find(".test-result-cell").html("Secure");
                        row.addClass("table-danger")
                    }
                    else
                    {
                        row.find(".test-result-cell").html("Result invalid or missing");
                        row.addClass("table-warning")
                    }
                }
                else
                {
                    if(testResult === "true")
                    {
                        row.find(".test-result-cell").html("Vulnerable");
                        row.addClass("table-danger")
                    }
                    else if(testResult === "false")
                    {
                        row.find(".test-result-cell").html("Secure");
                        row.addClass("table-success")
                    }
                    else
                    {
                        row.find(".test-result-cell").html("Result invalid or missing");
                        row.addClass("table-warning")
                    }
                }
                if(testCaptureName != null)
                {
                    row.find(".test-download-link").attr("href", "/captures/" + testCaptureName);
                }
                else
                {
                    row.find(".test-download-link").html("");
                }

                $("#device-test-table").append(row);
            });
        })
    $("#test-display-container").removeClass("d-none");       
    }
}

function displayAllTestResults()
{
    const apiurl = "/all_devices/";

    $.ajax({
        url:apiurl,
        dataType:"json",
        success:testListAllApiCallback
    })
}

function findDeviceAutocompleteList()
{
    const deviceListURL = "/devices/" //fill with proper url

    if(deviceListURL == "debug")
    {
        findDeviceAutocompleteListCallback(JSON.parse('{"devices":["test_debug_device","test_debug_device2"]}'), "success")
    }
    else
    {
        $.ajax({
            url:deviceListURL,
            dataType:"json",
            success:findDeviceAutocompleteListCallback
        })
    }
}

$(window).on('load', function(event) {
    if(window.location.pathname === "/list")
    {
        $("#search-button").on("click", submitDeviceTestSearch)
        $("#search-version-button").on("click", submitTestSearch)
        findDeviceAutocompleteList()
    }
    if(window.location.pathname === "/list_all")
    {
        displayAllTestResults();
    }
   });