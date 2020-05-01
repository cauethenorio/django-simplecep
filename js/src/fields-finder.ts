import {AutofillFieldDataType} from "./types";

export function querySimplecepAutofillFields(): Array<AutofillFieldDataType> {
    const selector = "[data-simplecep-autofill]";
    let fields: Array<AutofillFieldDataType> = [];

    document.querySelectorAll(selector).forEach((cepField: HTMLInputElement) => {
        try {
            const autoFill: AutofillFieldDataType = JSON.parse(cepField.dataset.simplecepAutofill);

            // delete the attr to avoid adding the same handler multiple times
            // when there are more than one form on the page
            delete cepField.dataset.simplecepAutofill;

            const {baseCepURL, dataFields} = autoFill;
            fields.push({cepField, baseCepURL, dataFields});
        } catch {}
    });

    return fields;
}
