const dataFieldTypes = ["state", "city", "district", "address"] as const;

export type DataFieldType = typeof dataFieldTypes[number];

export type AutofillFieldDataType = {
    cepField: HTMLInputElement;
    baseCepURL: string;
    dataFields: Array<{type: DataFieldType; selector: string}>;
};

export type HandlerParams = {
    fieldData: AutofillFieldDataType;
    getCepURL: (cep: string) => string;
    getDataFields: () => Array<{type: DataFieldType; els: Array<HTMLElement>}>;
    dispatch: (eventName: string, detail: any) => void;
    addListener: (
        eventName: string,
        listener: <D>(detail: D, e: CustomEvent<D>) => void
    ) => void;
};

export enum CepEvents {
    CepInputMasked = "simplecep-cep-input-masked",
    ValidCepInput = "simplecep-valid-cep-input",
    InvalidCepInput = "simplecep-invalid-cep-input",
    CepFetchStart = "simplecep-cep-fetch-start",
    CepFetchSuccess = "simplecep-cep-fetch-success",
    CepFetchError = "simplecep-cep-fetch-error",
    CepFetchIgnore = "simplecep-cep-fetch-ignore",
    CepFetchFinish = "simplecep-cep-fetch-finish"
}
