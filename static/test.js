function createOption(value)
{
    var element = document.createElement("option");
    element.value = value;
    element.innerHTML = value;
    return element;
}

function loadInterfacesCallback(result, code)
{
    if(code == "success")
    {
        var interfaces = result
        var interfaceSelect = $("#network-interface")
        interfaceSelect.html("")
        interfaceSelect.append(createOption("none"))
        interfaces.interfaces.forEach(interface => {
            interfaceSelect.append(createOption(interface))
        });
        
    }
    else{
        alert("failed to load list of interfaces")
    }
}

function loadInterfaces()
{
    const interfaceURL = "http://127.0.0.1:5000/interfaces/"

    if(interfaceURL == "debug")
    {
        loadInterfacesCallback(JSON.parse('{"interfaces":["interfaceA","interfaceB"]}'), "success")
    }
    else
    {
        $.ajax({
            url:interfaceURL,
            dataType:"json",
            success:loadInterfacesCallback
        })
    }
}

function createTestSubmissionDaoFromForm()
{
    var dao = new Object()
    dao.request = new Object()
    dao.request.ssid = $("#ssid").val()
    dao.request.password = $("#password").val()
    dao.request.interface = $("#network-interface").val()
    dao.request.description = $("#device-description").val()
    dao.request.mode = $('input[name="client-ap"]:checked').val();
    dao.request.tests = new Array()
    
    var testSelectors = $(".test-selection-row").each(function()
    {
        var selectorRow = $(this)
        var test =  new Object()
        var selector = selectorRow.find(".test-selector")
        var capture = selectorRow.find(".capture-packets")
        if(selector.is(":checked"))
        {
            test.name = selector.val()
            test.capture = capture.is(":checked")
            dao.request.tests.push(test)
        }
    })

    return JSON.stringify(dao)
}

function submissionSuccessCallback(response, code)
{
    if(code == "success")
    {
        alert("Test submission successful")
    }
}

function submitTestRequest(event)
{
    event.preventDefault();

    sumissionURL = "http://127.0.0.1:5000/testing"
    
    var dao = createTestSubmissionDaoFromForm()
    console.log(dao)

    $.ajax({
        url:sumissionURL,
        data:dao,
        dataType:"json",
        method:"POST",
        success:submissionSuccessCallback
    })
}

$(window).on('load', function(event) {
    $("#submit-tests-button").on("click", submitTestRequest);
    loadInterfaces()
});