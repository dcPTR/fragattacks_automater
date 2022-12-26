function testListApiCallback(result, code)
{
    console.log("API CALLBACK");
    console.log(result);
    console.log(code);
    console.log("API CALLBACK END");
    // stringify result to get the json string
    result = JSON.stringify(result);
    if(code === "success")
    {
        console.log(result);
        var testList = JSON.parse(result);
        console.log(testList);
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
    else
    {
        // Error handling here
    }
}

function callTestListApi(deviceName)
{
    const apiurl = "http://127.0.0.1:5000/devices/"; //put real api endpoint url here

    if(deviceName === "test_debug_device")
    {
        testJson = '{"device":{"name":"Test Device","description":"Test Description","version":"1.23.486_test"},"tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]}';
        testListApiCallback(testJson, "success");
    }
    else
    {
        console.log("API CALL");
        // cal ajax and console log the result
        out = $.ajax({
            url: apiurl + deviceName,
            type: "GET",
            dataType: "json",
            success: function(result, code) {
                console.log("API SUCCESS");
                testListApiCallback(result, code);
            },
            error: function(result, code) {
                // console.log(result);
                // console.log(code);
                console.log("ERROR");
                testListApiCallback(result, code);
                }
        });



    }
}

function submitTestSearch(event)
{
    event.preventDefault();
    var deviceName = $("#device-name").val();
    callTestListApi(deviceName);
}

$(window).on('load', function(event) {
    $("#search-button").on("click", submitTestSearch);
   });