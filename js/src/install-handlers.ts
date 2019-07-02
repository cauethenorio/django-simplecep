import {AutofillFieldDataType} from "./fields-finder";

export type HandlerParams = {
    fieldData: AutofillFieldDataType;
    getCepURL: (cep: string) => string;
    getDataFields: ReturnType<typeof createDataFieldsGetter>;
    dispatch: ReturnType<typeof createDispatcher>;
    addListener: ReturnType<typeof createListenerFactory>;
};

const createDispatcher = (el: HTMLElement) => (eventName: string, detail: any) => {
    const event = new CustomEvent(eventName, {detail});
    el.dispatchEvent(event);
};

const createListenerFactory = (el: HTMLElement) => <D>(
    eventName: string,
    listener: (detail: D, e: CustomEvent<D>) => any
) =>
    el.addEventListener(eventName, e =>
        listener((e as CustomEvent<D>).detail, e as CustomEvent<D>)
    );

const createDataFieldsGetter = (
    dataFields: AutofillFieldDataType["dataFields"]
) => () =>
    dataFields.map(({type, selector}) => ({
        type,
        els: Array.prototype.slice
            .call(document.querySelectorAll(selector))
            .filter((node: HTMLElement | null) => node != null)
    }));

export function installHandlers(
    fieldData: AutofillFieldDataType,
    handlers: Array<(args: HandlerParams) => void>
) {
    const {baseCepURL, dataFields} = fieldData;
    const getCepURL = (cep: string): string => baseCepURL.replace("00000000", cep);
    const getDataFields = createDataFieldsGetter(dataFields);

    const dispatch = createDispatcher(fieldData.cepField);
    const addListener = createListenerFactory(fieldData.cepField);

    const handlersParam = {getCepURL, getDataFields, fieldData, dispatch, addListener};
    handlers.forEach(handler => handler(handlersParam));
}
