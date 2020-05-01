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
    quickDispatchEvent: (eventName: string, detail: any) => void;
    quickAddEventListener: <D>(
        eventName: string,
        listener: (detail: D, e: CustomEvent<D>) => void
    ) => () => void;
};

export enum CepEvents {
    CEPValueCleaned = "simplecep.CEPValueCleaned",
    ValidCepInput = "simplecep.ValidCepInput",
    InvalidCepInput = "simplecep.InvalidCepInput",
    CepFetchStart = "simplecep.CepFetchStart",
    CepFetchSuccess = "simplecep.CepFetchSuccess",
    CepFetchError = "simplecep.CepFetchError",
    CepFetchFinish = "simplecep.CepFetchFinish",
    CepFieldsAutofilled = "simplecep.CepFieldsAutofilled",

    InstallHandler = "simplecep.installHandler",
    removeHandler = "simplecep.removeHandler",
}

export type InstallHandlerCustomEvent = CustomEvent<{
    handlerName: string;
    installer: (bla: any) => () => undefined;
}>;

export type UninstallHandlerCustomEvent = CustomEvent<{handlerName: string}>;
