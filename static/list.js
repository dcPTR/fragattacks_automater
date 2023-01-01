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

        row.find(".test-name-cell").html(name);
        row.find(".test-result-cell").html(testResult);
        if(testResult == "true")
        {
            row.addClass("table-success")
        }
        else if(testResult == "false")
        {
            row.addClass("table-danger")
        }
        else
        {
            row.addClass("table-warning")
        }
        $("#device-test-table").append(row);
    });

    $("#test-display-container").removeClass("d-none");
}

function testListApiCallback(result, code)
{
    if(code = "success")
    {
        try{
            currentDeviceListObject = JSON.parse(result);
            findtestVersions()
            $("#test-version-form-container").removeClass("d-none")
        }
        catch( error )
        {
            displayDeviceError("Couldn't parse the server response. " + error)
            return
        }
    }
    else
    {
        displayDeviceError("Couldn't recieve device information. Code:" + code)
    }
}

function callTestListApi(deviceName)
{
    const apiurl = "https://jsonplaceholder.typicode.com/todos/1/"; //put real api endpoint url here

    if(deviceName === "test_debug_device")
    {
        testJson = '[{"device":{"name":"Test Device","description":"Test Description","version":"1.23.486_test"},"tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]}]';
        testListApiCallback(testJson, "success");
    }
    else if(deviceName === "test_debug_device2")
    {
        testJson = '[{"device":{"name":"Test Device2","description":"Test Description","version":"1.23.486_test"},"tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]},\
        {"device":{"name":"Test Device2","description":"Test Description","version":"1.24.489_test"},"tests":[["testsucccess","false"],["testfail","false"],["testunknown","true"]]}]';
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
    if(code = "success")
    {
        try{
            deviceAutocompleteList = result.devices;
            $("#device-name").autocomplete(
                {
                    source:deviceAutocompleteList
                }
              );
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

function findDeviceAutocompleteList()
{
    const deviceListURL = "http://127.0.0.1:5000/devices/" //fill with proper url

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
    $("#search-button").on("click", submitDeviceTestSearch);
    $("#search-version-button").on("click", submitTestSearch);
    findDeviceAutocompleteList()
   });