import {HandlerParams, CepEvents} from "../types";

export function cepMaskHandler({dispatch, addListener}: HandlerParams) {
    addListener("input", (detail, e: Event) => {
        if (e.target instanceof HTMLInputElement) {
            const original = e.target.value;
            let formatted = original.replace(/\D/g, "");

            if (formatted.length > 5) {
                formatted = `${formatted.substr(0, 5)}-${formatted.substr(5, 3)}`;
            }

            e.target.value = formatted;
            dispatch(CepEvents.CepInputMasked, formatted);
        }
    });
}
