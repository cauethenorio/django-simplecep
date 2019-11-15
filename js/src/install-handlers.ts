import {HandlerParams, AutofillFieldDataType} from "./types";

const createDispatcher = (el: HTMLElement): HandlerParams["dispatch"] => (
    eventName: string,
    detail: any
) => {
    const event = new CustomEvent(eventName, {detail});
    console.log("dispatching " + eventName);
    el.dispatchEvent(event);
};

const createListenerFactory = (el: HTMLElement): HandlerParams["addListener"] => <D>(
    eventName: string,
    listener: (detail: D, e: CustomEvent<D>) => any
) =>
    el.addEventListener(eventName, e =>
        listener((e as CustomEvent<D>).detail, e as CustomEvent<D>)
    );

const createDataFieldsGetter = (
    dataFields: AutofillFieldDataType["dataFields"]
): HandlerParams["getDataFields"] => () =>
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
    const getCepURL: HandlerParams["getCepURL"] = (cep: string): string =>
        baseCepURL.replace("00000000", cep);
    const getDataFields = createDataFieldsGetter(dataFields);

    const dispatch = createDispatcher(fieldData.cepField);
    const addListener = createListenerFactory(fieldData.cepField);

    const handlersParam = {getCepURL, getDataFields, fieldData, dispatch, addListener};
    handlers.forEach(handler => handler(handlersParam));
}
