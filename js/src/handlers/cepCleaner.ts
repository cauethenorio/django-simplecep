import {HandlerParams, CepEvents} from "../types";

/*
  This handler is responsible for cleaning the values user inputs on the CEP field.

  It listens for 'input' event on the CEP input field and dispatches:
    - CepEvents.CEPValueCleaned
      With the cleaned value after the user changes the input value
 */

export const cepCleanerInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "cepCleaner",
        installer: cepMaskInstaller,
    },
});

function cepMaskInstaller({fieldData, quickDispatchEvent, quickAddEventListener}: HandlerParams) {
    return quickAddEventListener("input", (_, e) => {
        if (e.target instanceof HTMLInputElement) {
            const {value} = e.target;

            let [formatted, start, end] = format(e.target);
            let selectionDelta = 0;

            if (formatted.length > 5) {
                formatted = `${formatted.substr(0, 5)}-${formatted.substr(5, 3)}`;
                if (start > 5) {
                    selectionDelta += 1;
                }
            }

            e.target.value = formatted;
            e.target.selectionStart = Math.max(start + selectionDelta, 0);
            e.target.selectionEnd = Math.max(end + selectionDelta, 0);
            quickDispatchEvent(CepEvents.CEPValueCleaned, formatted);
        }
    });
}

const clean = (value: string): string => value.replace(/\D/g, "");

const format = (el: HTMLInputElement): [string, number, number] => {
    const [start, end] = [el.selectionStart, el.selectionEnd].map((i) => {
        const cleaned = clean(el.value.slice(0, i));
        return i + (cleaned.length - i);
    });
    return [clean(el.value), start, end];
};
