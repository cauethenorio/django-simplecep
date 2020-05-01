import {CepEvents, HandlerParams} from "../types";

export const cepLoadingIndicatorInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "cepLoadingIndicator",
        installer: cepLoadingIndicatorInstaller,
    },
});

export function cepLoadingIndicatorInstaller({quickAddEventListener, fieldData}: HandlerParams) {
    const cepField = fieldData.cepField;
    const loadingIndicatorId = `${cepField.id}_loading-indicator`;
    const loadingIndicator = document.getElementById(loadingIndicatorId);

    if (loadingIndicator != null) {
        quickAddEventListener(CepEvents.CepFetchStart, () => {
            positionLoadingIndicator(cepField, loadingIndicator);
            loadingIndicator.classList.add("visible");
        });
        quickAddEventListener(CepEvents.CepFetchFinish, () => {
            loadingIndicator.classList.remove("visible");
        });
    }
}

function positionLoadingIndicator(cepField: HTMLElement, loadingIndicator: HTMLElement) {
    const {style} = loadingIndicator;
    const {offsetTop, offsetLeft, offsetWidth, offsetHeight} = cepField;

    style.top = `${offsetTop}px`;
    style.left = `${offsetLeft + offsetWidth - loadingIndicator.offsetWidth}px`;
    style.height = `${offsetHeight}px`;
}
