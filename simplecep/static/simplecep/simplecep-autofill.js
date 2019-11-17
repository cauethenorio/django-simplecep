(function () {
    'use strict';

    function querySimplecepAutofillFields() {
        var selector = "[data-simplecep-autofill]";
        var fields = [];
        document.querySelectorAll(selector).forEach(function (cepField) {
            try {
                var autoFill = JSON.parse(cepField.dataset.simplecepAutofill);
                // delete the attr to avoid adding the same handler multiple times
                delete cepField.dataset.simplecepAutofill;
                var baseCepURL = autoFill.baseCepURL, dataFields = autoFill.dataFields;
                fields.push({ cepField: cepField, baseCepURL: baseCepURL, dataFields: dataFields });
            }
            catch (_a) { }
        });
        return fields;
    }

    var CepEvents;
    (function (CepEvents) {
        CepEvents["CepInputMasked"] = "simplecep-cep-input-masked";
        CepEvents["ValidCepInput"] = "simplecep-valid-cep-input";
        CepEvents["InvalidCepInput"] = "simplecep-invalid-cep-input";
        CepEvents["CepFetchStart"] = "simplecep-cep-fetch_url-start";
        CepEvents["CepFetchSuccess"] = "simplecep-cep-fetch_url-success";
        CepEvents["CepFetchError"] = "simplecep-cep-fetch_url-error";
        CepEvents["CepFetchIgnore"] = "simplecep-cep-fetch_url-ignore";
        CepEvents["CepFetchFinish"] = "simplecep-cep-fetch_url-finish";
    })(CepEvents || (CepEvents = {}));

    function cleanCep(cep) {
        var match = /^([0-9]{5})[\- ]?([0-9]{3})$/.exec(cep);
        return match != null ? match.slice(1, 3).join("") : null;
    }
    function cepInputHandler(_a) {
        var dispatch = _a.dispatch, addListener = _a.addListener;
        addListener(CepEvents.CepInputMasked, function (cepValue, e) {
            var cleanedCep = cleanCep(cepValue);
            if (cleanedCep != null) {
                dispatch(CepEvents.ValidCepInput, cleanedCep);
            }
            else {
                dispatch(CepEvents.InvalidCepInput, cepValue);
            }
        });
    }

    var fetchCepData = function (url) {
        return fetch(url).then(function (response) {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            }
            else {
                var error = new Error(response.statusText || response.status.toString());
                error.response = response;
                return Promise.reject(error);
            }
        });
    };
    function fetchCepHandler(_a) {
        var dispatch = _a.dispatch, addListener = _a.addListener, getCepURL = _a.getCepURL;
        var lastRequestedCep;
        addListener(CepEvents.ValidCepInput, function (cep) {
            var cepURL = getCepURL(cep);
            lastRequestedCep = cep;
            fetchCepData(cepURL)
                .then(function (response) {
                return dispatch(lastRequestedCep === cep
                    ? CepEvents.CepFetchSuccess
                    : CepEvents.CepFetchIgnore, response);
            }, function (error) { return dispatch(CepEvents.CepFetchError, error); })
                .then(function (value) { return dispatch(CepEvents.CepFetchFinish, value); });
            dispatch(CepEvents.CepFetchStart, cepURL);
        });
    }

    function cepMaskHandler(_a) {
        var dispatch = _a.dispatch, addListener = _a.addListener;
        addListener("input", function (detail, e) {
            if (e.target instanceof HTMLInputElement) {
                var original = e.target.value;
                var formatted = original.replace(/\D/g, "");
                if (formatted.length > 5) {
                    formatted = formatted.substr(0, 5) + "-" + formatted.substr(5, 3);
                }
                e.target.value = formatted;
                dispatch(CepEvents.CepInputMasked, formatted);
            }
        });
    }

    function fillFields(_a) {
        var getDataFields = _a.getDataFields, dispatch = _a.dispatch, addListener = _a.addListener, getCepURL = _a.getCepURL;
        var dataFields = getDataFields();
        addListener(CepEvents.CepFetchSuccess, function (cepData) {
            dataFields.forEach(function (_a) {
                var type = _a.type, els = _a.els;
                var val = cepData[type];
                if (val != null) {
                    els.forEach(function (e) {
                        if (e instanceof HTMLInputElement) {
                            e.value = val;
                        }
                    });
                }
            });
        });
    }

    function positionLoadingIndicator(cepField, loadingIndicator) {
        var style = loadingIndicator.style;
        var offsetTop = cepField.offsetTop, offsetLeft = cepField.offsetLeft, offsetWidth = cepField.offsetWidth, offsetHeight = cepField.offsetHeight;
        style.top = offsetTop + "px";
        style.left = offsetLeft + offsetWidth - loadingIndicator.offsetWidth + "px";
        style.height = offsetHeight + "px";
    }
    function loadingIndicatorHandler(_a) {
        var addListener = _a.addListener, fieldData = _a.fieldData;
        var cepField = fieldData.cepField;
        var loadingIndicatorId = cepField.id + "_loading-indicator";
        var loadingIndicator = document.getElementById(loadingIndicatorId);
        if (loadingIndicator != null) {
            addListener(CepEvents.CepFetchStart, function () {
                positionLoadingIndicator(cepField, loadingIndicator);
                loadingIndicator.classList.add("visible");
            });
            addListener(CepEvents.CepFetchFinish, function () {
                loadingIndicator.classList.remove("visible");
            });
        }
    }

    var defaultHandlers = [
        cepInputHandler,
        fetchCepHandler,
        cepMaskHandler,
        fillFields,
        loadingIndicatorHandler
    ];

    var createDispatcher = function (el) { return function (eventName, detail) {
        var event = new CustomEvent(eventName, { detail: detail });
        console.log("dispatching " + eventName);
        el.dispatchEvent(event);
    }; };
    var createListenerFactory = function (el) { return function (eventName, listener) {
        return el.addEventListener(eventName, function (e) {
            return listener(e.detail, e);
        });
    }; };
    var createDataFieldsGetter = function (dataFields) { return function () {
        return dataFields.map(function (_a) {
            var type = _a.type, selector = _a.selector;
            return ({
                type: type,
                els: Array.prototype.slice
                    .call(document.querySelectorAll(selector))
                    .filter(function (node) { return node != null; })
            });
        });
    }; };
    function installHandlers(fieldData, handlers) {
        var baseCepURL = fieldData.baseCepURL, dataFields = fieldData.dataFields;
        var getCepURL = function (cep) {
            return baseCepURL.replace("00000000", cep);
        };
        var getDataFields = createDataFieldsGetter(dataFields);
        var dispatch = createDispatcher(fieldData.cepField);
        var addListener = createListenerFactory(fieldData.cepField);
        var handlersParam = { getCepURL: getCepURL, getDataFields: getDataFields, fieldData: fieldData, dispatch: dispatch, addListener: addListener };
        handlers.forEach(function (handler) { return handler(handlersParam); });
    }

    /* find all CEP fields in the page and install default defaultHandlers in all of them */
    querySimplecepAutofillFields().map(function (cepFieldData) {
        return installHandlers(cepFieldData, defaultHandlers);
    });

}());
