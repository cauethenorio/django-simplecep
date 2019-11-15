import {HandlerParams, CepEvents} from "../types";

export function cleanCep(cep: string): string | null {
    const match = /^([0-9]{5})[\- ]?([0-9]{3})$/.exec(cep);
    return match != null ? match.slice(1, 3).join("") : null;
}

export function cepInputHandler({dispatch, addListener}: HandlerParams) {
    addListener(CepEvents.CepInputMasked, (cepValue, e: Event) => {
        const cleanedCep = cleanCep((cepValue as unknown) as string);

        if (cleanedCep != null) {
            dispatch(CepEvents.ValidCepInput, cleanedCep);
        } else {
            dispatch(CepEvents.InvalidCepInput, cepValue);
        }
    });
}
