(function () {
    'use strict';

    function querySimplecepAutofillFields() {
        var selector = "[data-simplecep-autofill]";
        var fields = [];
        document.querySelectorAll(selector).forEach(function (cepField) {
            try {
                var autoFill = JSON.parse(cepField.dataset.simplecepAutofill);
                // delete the attr to avoid adding the same handler multiple times
                // when there are more than one form on the page
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
        CepEvents["CEPValueCleaned"] = "simplecep.CEPValueCleaned";
        CepEvents["ValidCepInput"] = "simplecep.ValidCepInput";
        CepEvents["InvalidCepInput"] = "simplecep.InvalidCepInput";
        CepEvents["CepFetchStart"] = "simplecep.CepFetchStart";
        CepEvents["CepFetchSuccess"] = "simplecep.CepFetchSuccess";
        CepEvents["CepFetchError"] = "simplecep.CepFetchError";
        CepEvents["CepFetchFinish"] = "simplecep.CepFetchFinish";
        CepEvents["CepFieldsAutofilled"] = "simplecep.CepFieldsAutofilled";
        CepEvents["InstallHandler"] = "simplecep.installHandler";
        CepEvents["removeHandler"] = "simplecep.removeHandler";
    })(CepEvents || (CepEvents = {}));

    /*
      This handler is responsible for cleaning the values user inputs on the CEP field.

      It listens for 'input' event on the CEP input field and dispatches:
        - CepEvents.CEPValueCleaned
          With the cleaned value after the user changes the input value
     */
    var cepCleanerInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "cepCleaner",
            installer: cepMaskInstaller,
        },
    });
    function cepMaskInstaller(_a) {
        var fieldData = _a.fieldData, quickDispatchEvent = _a.quickDispatchEvent, quickAddEventListener = _a.quickAddEventListener;
        return quickAddEventListener("input", function (_, e) {
            if (e.target instanceof HTMLInputElement) {
                var value = e.target.value;
                var _a = format(e.target), formatted = _a[0], start = _a[1], end = _a[2];
                var selectionDelta = 0;
                if (formatted.length > 5) {
                    formatted = formatted.substr(0, 5) + "-" + formatted.substr(5, 3);
                    if (start > 5) {
                        selectionDelta += 1;
                    }
                }
                e.target.value = formatted;
                e.target.selectionStart = Math.max(start + selectionDelta, 0);
                e.target.selectionEnd = Math.max(end + selectionDelta, 0);
                quickDispatchEvent(CepEvents.CEPValueCleaned, formatted);
            }
        });
    }
    var clean = function (value) { return value.replace(/\D/g, ""); };
    var format = function (el) {
        var _a = [el.selectionStart, el.selectionEnd].map(function (i) {
            var cleaned = clean(el.value.slice(0, i));
            return i + (cleaned.length - i);
        }), start = _a[0], end = _a[1];
        return [clean(el.value), start, end];
    };

    /*
      This handler is responsible for checking if the cleaned value is a valid CEP or not.

        It listen for CepEvents.CEPValueCleaned events and dispatches:
          - CepEvents.ValidCepInput
            With the cleaned value when it's a valid CEP value

          - CepEvents.InvalidCepInput
            With the cleaned value when it's not a valid CEP value
     */
    var cepValidatorInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "cepValidator",
            installer: cepValidatorInstaller,
        },
    });
    function cepValidatorInstaller(_a) {
        var quickDispatchEvent = _a.quickDispatchEvent, quickAddEventListener = _a.quickAddEventListener;
        return quickAddEventListener(CepEvents.CEPValueCleaned, function (cepValue, e) {
            var cleanedCep = cleanCep(cepValue);
            if (cleanedCep != null) {
                quickDispatchEvent(CepEvents.ValidCepInput, cleanedCep);
            }
            else {
                quickDispatchEvent(CepEvents.InvalidCepInput, cepValue);
            }
        });
    }
    function cleanCep(cep) {
        var match = /^([0-9]{5})[\- ]?([0-9]{3})$/.exec(cep);
        return match != null ? match.slice(1, 3).join("") : null;
    }

    /*
      This handler is responsible for fetching CEP data when a valid CEP is input.

        It listens for CepEvents.ValidCepInput events and dispatches:
          - CepEvents.CepFetchStart
            With the cepURL when it request for CEP data

          - CepEvents.CepFetchSuccess
            With fetched CEP data on success

          - CepEvents.CepFetchError
            With the error when it fails fetching the data

          - CepEvents.CepFetchFinish
            With CEP data or error, when the request is finished (with error or not).
     */
    var cepFetcherInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "cepFetcher",
            installer: cepFetcherInstaller,
        },
    });
    function cepFetcherInstaller(_a) {
        var quickDispatchEvent = _a.quickDispatchEvent, quickAddEventListener = _a.quickAddEventListener, getCepURL = _a.getCepURL;
        return quickAddEventListener(CepEvents.ValidCepInput, function (cep) {
            var cepURL = getCepURL(cep);
            quickDispatchEvent(CepEvents.CepFetchStart, cepURL);
            fetchCepData(cepURL)
                .then(function (response) { return quickDispatchEvent(CepEvents.CepFetchSuccess, response); }, function (error) { return quickDispatchEvent(CepEvents.CepFetchError, error); })
                .then(function (value) { return quickDispatchEvent(CepEvents.CepFetchFinish, value); });
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

    var cepLoadingIndicatorInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "cepLoadingIndicator",
            installer: cepLoadingIndicatorInstaller,
        },
    });
    function cepLoadingIndicatorInstaller(_a) {
        var quickAddEventListener = _a.quickAddEventListener, fieldData = _a.fieldData;
        var cepField = fieldData.cepField;
        var loadingIndicatorId = cepField.id + "_loading-indicator";
        var loadingIndicator = document.getElementById(loadingIndicatorId);
        if (loadingIndicator != null) {
            quickAddEventListener(CepEvents.CepFetchStart, function () {
                positionLoadingIndicator(cepField, loadingIndicator);
                loadingIndicator.classList.add("visible");
            });
            quickAddEventListener(CepEvents.CepFetchFinish, function () {
                loadingIndicator.classList.remove("visible");
            });
        }
    }
    function positionLoadingIndicator(cepField, loadingIndicator) {
        var style = loadingIndicator.style;
        var offsetTop = cepField.offsetTop, offsetLeft = cepField.offsetLeft, offsetWidth = cepField.offsetWidth, offsetHeight = cepField.offsetHeight;
        style.top = offsetTop + "px";
        style.left = offsetLeft + offsetWidth - loadingIndicator.offsetWidth + "px";
        style.height = offsetHeight + "px";
    }

    /*
      This handler is responsible for locking the CEP data fields, making them
      readonly while the CEP data is fetch.

      So users won't be frustrated if they fill the fields with their own data
      and then it's overwritten by the autofill feature.
     */
    var cepFieldsLockerInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "cepFieldsLocker",
            installer: cepFieldsLockerInstaller,
        },
    });
    function cepFieldsLockerInstaller(_a) {
        var getDataFields = _a.getDataFields, quickAddEventListener = _a.quickAddEventListener;
        var lockedFields = [];
        function restoreFields() {
            lockedFields.forEach(function (_a) {
                var field = _a.field, oldValue = _a.oldValue;
                if (oldValue === "") {
                    field.removeAttribute("readonly");
                }
                else {
                    field.setAttribute("readonly", oldValue);
                }
            });
            lockedFields = [];
        }
        var removeCepFetchStartListener = quickAddEventListener(CepEvents.CepFetchStart, function () {
            var fields = getDataFields();
            fields.forEach(function (_a) {
                var type = _a.type, els = _a.els;
                els.forEach(function (field) {
                    if (formFieldsTags.includes(field.tagName)) {
                        lockedFields.push({
                            field: field,
                            oldValue: field.getAttribute("readonly") || "",
                        });
                        field.setAttribute("readonly", "readonly");
                    }
                });
            });
        });
        var removeCepFetchErrorListener = quickAddEventListener(CepEvents.CepFetchError, restoreFields);
        var removeCepFieldsAutofilledListener = quickAddEventListener(CepEvents.CepFieldsAutofilled, restoreFields);
        return function () {
            removeCepFetchStartListener();
            removeCepFetchErrorListener();
            removeCepFieldsAutofilledListener();
        };
    }
    var formFieldsTags = ["INPUT", "SELECT", "TEXTAREA"];

    var cepFieldsFillerInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "cepFieldsFiller",
            installer: cepFieldsFillerInstaller,
        },
    });
    function cepFieldsFillerInstaller(_a) {
        var getDataFields = _a.getDataFields, quickAddEventListener = _a.quickAddEventListener, quickDispatchEvent = _a.quickDispatchEvent;
        return quickAddEventListener(CepEvents.CepFetchSuccess, function (cepData) {
            var fields = getDataFields();
            fields.forEach(function (_a) {
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
            quickDispatchEvent(CepEvents.CepFieldsAutofilled, { fields: fields, cepData: cepData });
        });
    }

    var cepFieldsAutoFocusInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
        detail: {
            handlerName: "focus-next",
            installer: cepFieldsAutoFocusInstaller,
        },
    });
    function cepFieldsAutoFocusInstaller(_a) {
        var quickAddEventListener = _a.quickAddEventListener;
        return quickAddEventListener(CepEvents.CepFieldsAutofilled, function (_a) {
            var fields = _a.fields, cepData = _a.cepData;
            for (var _i = 0, fields_1 = fields; _i < fields_1.length; _i++) {
                var _b = fields_1[_i], type = _b.type, els = _b.els;
                // search for the first field which returned with no data
                if (cepData[type] == null) {
                    for (var _c = 0, els_1 = els; _c < els_1.length; _c++) {
                        var el = els_1[_c];
                        // search for the first element which is a form field
                        // attached to the field type
                        if (formFieldsTags$1.indexOf(el.tagName) >= 0) {
                            el.focus();
                            return;
                        }
                    }
                }
            }
        });
    }
    var formFieldsTags$1 = ["INPUT", "SELECT", "TEXTAREA"];

    var defaultInstallerEvents = [
        cepCleanerInstallEvent,
        cepValidatorInstallEvent,
        cepFetcherInstallEvent,
        cepLoadingIndicatorInstallEvent,
        cepFieldsLockerInstallEvent,
        cepFieldsFillerInstallEvent,
        cepFieldsAutoFocusInstallEvent,
    ];

    var createDispatcher = function (el) { return function (eventName, detail) {
        var event = new CustomEvent(eventName, { detail: detail });
        console.log("Dispatching " + eventName + ".");
        el.dispatchEvent(event);
    }; };
    var createListenerFactory = function (el) { return function (eventName, listener) {
        var listenerWrapper = function (e) { return listener(e.detail, e); };
        el.addEventListener(eventName, listenerWrapper);
        console.log("Event listener registered for '" + eventName + "'.");
        return function () { return el.removeEventListener(eventName, listenerWrapper); };
    }; };
    function createQuickEventsFuncsFor(el) {
        return {
            quickAddEventListener: createListenerFactory(el),
            quickDispatchEvent: createDispatcher(el),
        };
    }

    var createDataFieldsGetter = function (dataFields) { return function () {
        return dataFields.map(function (_a) {
            var type = _a.type, selector = _a.selector;
            return ({
                type: type,
                els: Array.prototype.slice
                    .call(document.querySelectorAll(selector))
                    .filter(function (node) { return node != null; }),
            });
        });
    }; };
    function getHandlerInstallerParameters(fieldData) {
        /* create an object with useful data to be sent as param to handler installers */
        var baseCepURL = fieldData.baseCepURL, dataFields = fieldData.dataFields;
        var getCepURL = function (cep) {
            return baseCepURL.replace("00000000", cep);
        };
        var getDataFields = createDataFieldsGetter(dataFields);
        var _a = createQuickEventsFuncsFor(fieldData.cepField), quickAddEventListener = _a.quickAddEventListener, quickDispatchEvent = _a.quickDispatchEvent;
        /* when you install a CEP field handler, these are the parameters your
        installer function will receive */
        return {
            getCepURL: getCepURL,
            getDataFields: getDataFields,
            fieldData: fieldData,
            quickDispatchEvent: quickDispatchEvent,
            quickAddEventListener: quickAddEventListener,
        };
    }
    function enableHandlersInstall(fieldData) {
        // object with all installed handlers as key
        // and a func to uninstall them as value
        var installedHandlers = {};
        var cepField = fieldData.cepField;
        cepField.addEventListener(CepEvents.InstallHandler, (function (event) {
            var _a = event.detail, installer = _a.installer, handlerName = _a.handlerName;
            /* it there's already a handler registered with that name, unregister it.
            So it's easier for the user to replace any handler */
            if (installedHandlers[handlerName] != null) {
                var previousHandlerUninstall = installedHandlers[handlerName];
                previousHandlerUninstall();
                console.log("Handler '" + handlerName + "' removed to be replaced.");
            }
            var handlerInstallerParams = getHandlerInstallerParameters(fieldData);
            installedHandlers[handlerName] = installer(handlerInstallerParams);
            console.log("Handler '" + handlerName + "' installed.");
        }));
        cepField.addEventListener(CepEvents.removeHandler, (function (event) {
            var handlerName = event.detail.handlerName;
            installedHandlers[handlerName]();
            console.log("Handler '" + handlerName + "' removed.");
        }));
    }

    /* find all CEP fields in the page and install default defaultHandlers in all of them */
    querySimplecepAutofillFields().map(function (cepFieldData) {
        enableHandlersInstall(cepFieldData);
        defaultInstallerEvents.forEach(function (event) { return cepFieldData.cepField.dispatchEvent(event); });
    });

}());
