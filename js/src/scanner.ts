const cepFields = <const> ["state", "city", "district", "address"];


function withPrefix(attr: string): string {
    return `simplecep-${attr}`;
}


const cepFieldsAttributes = cepFields.map(
    field => `${withPrefix(field)}-field-id`
);


const hyphenized = (str: string): string => (
    str.replace(/([a-z][A-Z])/g, g => g[0] + '-' + g[1].toLowerCase())
);


function extractCepFieldsMapFromNode(node: HTMLElement): {[key: string]: string} {
    return Object.keys(node.dataset).reduce((obj: any, attr) => {
        const fieldIndex = cepFieldsAttributes.indexOf(hyphenized(attr));

        if (fieldIndex > -1) {
            const fieldType = cepFields[fieldIndex];
            obj[fieldType] = node.dataset[attr];
        }

        return obj;
    }, {});
}


type FieldDataType = {
    cepFieldId: string,
    getCepURL: string,
    fieldsIds: {[key: string]: string},
}

export function scanSimpleCepFields(): Array<FieldDataType> {
    const selector = `[data-${withPrefix('autocomplete')}]`;
    let fields: Array<FieldDataType> = [];

    document.querySelectorAll(selector).forEach(
        (node: HTMLElement) => {
            fields.push({
                cepFieldId: node.id,
                getCepURL: node.dataset.simplecepGetCepUrl,
                fieldsIds: extractCepFieldsMapFromNode(node)
            })
        }
    );

    return fields;
}
