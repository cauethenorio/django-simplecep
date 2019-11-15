import {CepEvents, DataFieldType, HandlerParams} from "../types";

export function fillFields({
    getDataFields,
    dispatch,
    addListener,
    getCepURL
}: HandlerParams) {
    const dataFields = getDataFields();
    addListener(CepEvents.CepFetchSuccess, (cepData: any) => {
        dataFields.forEach(({type, els}) => {
            const val = cepData[type];
            if (val != null) {
                els.forEach(e => {
                    if (e instanceof HTMLInputElement) {
                        e.value = val;
                    }
                });
            }
        });
    });
}
