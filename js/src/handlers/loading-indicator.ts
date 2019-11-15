import {CepEvents, HandlerParams} from "../types";

function positionLoadingIndicator(
    cepField: HTMLElement,
    loadingIndicator: HTMLElement
) {
    const {style} = loadingIndicator;
    const {offsetTop, offsetLeft, offsetWidth, offsetHeight} = cepField;

    style.top = `${offsetTop}px`;
    style.left = `${offsetLeft + offsetWidth - loadingIndicator.offsetWidth}px`;
    style.height = `${offsetHeight}px`;
}

export function loadingIndicatorHandler({addListener, fieldData}: HandlerParams) {
    const cepField = fieldData.cepField;
    const loadingIndicatorId = `${cepField.id}_loading-indicator`;
    const loadingIndicator = document.getElementById(loadingIndicatorId);

    if (loadingIndicator != null) {
        addListener(CepEvents.CepFetchStart, () => {
            positionLoadingIndicator(cepField, loadingIndicator);
            loadingIndicator.classList.add("visible");
        });
        addListener(CepEvents.CepFetchFinish, () => {
            loadingIndicator.classList.remove("visible");
        });
    }
}
