import {HandlerParams, CepEvents} from "../types";

/*
  This handler is responsible for checking if the cleaned value is a valid CEP or not.

    It listen for CepEvents.CEPValueCleaned events and dispatches:
      - CepEvents.ValidCepInput
        With the cleaned value when it's a valid CEP value

      - CepEvents.InvalidCepInput
        With the cleaned value when it's not a valid CEP value
 */

export const cepValidatorInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "cepValidator",
        installer: cepValidatorInstaller,
    },
});

function cepValidatorInstaller({quickDispatchEvent, quickAddEventListener}: HandlerParams) {
    return quickAddEventListener(
        CepEvents.CEPValueCleaned,
        (cepValue: string, e: CustomEvent<string>): void => {
            const cleanedCep = cleanCep((cepValue as unknown) as string);

            if (cleanedCep != null) {
                quickDispatchEvent(CepEvents.ValidCepInput, cleanedCep);
            } else {
                quickDispatchEvent(CepEvents.InvalidCepInput, cepValue);
            }
        }
    );
}

function cleanCep(cep: string): string | null {
    const match = /^([0-9]{5})[\- ]?([0-9]{3})$/.exec(cep);
    return match != null ? match.slice(1, 3).join("") : null;
}
