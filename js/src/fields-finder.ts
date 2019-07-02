const dataFieldTypes = ["state", "city", "district", "address"] as const;

type DataFieldType = typeof dataFieldTypes[number];

export type AutofillFieldDataType = {
    cepField: HTMLInputElement;
    baseCepURL: string;
    dataFields: [{type: DataFieldType; selector: string}];
};

export function querySimplecepAutofillFields(): Array<AutofillFieldDataType> {
    const selector = "[data-simplecep-autofill]";
    let fields: Array<AutofillFieldDataType> = [];

    document.querySelectorAll(selector).forEach((cepField: HTMLInputElement) => {
        try {
            const autoFill: AutofillFieldDataType = JSON.parse(
                cepField.dataset.simplecepAutofill
            );

            // delete the attr to avoid adding the same handler multiple times
            delete cepField.dataset.simplecepAutofill;
            const {baseCepURL, dataFields} = autoFill;
            fields.push({cepField, baseCepURL, dataFields});
        } catch {}
    });

    return fields;
}
