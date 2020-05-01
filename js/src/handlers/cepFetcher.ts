import {CepEvents, DataFieldType, HandlerParams} from "../types";

type CepDataType = {[key in DataFieldType]: string | null};

/*
  This handler is responsible for fetching CEP data when a valid CEP is input.

    It listens for CepEvents.ValidCepInput events and dispatches:
      - CepEvents.CepFetchStart
        With the cepURL when it request for CEP data

      - CepEvents.CepFetchSuccess
        With fetched CEP data on success

      - CepEvents.CepFetchError
        With the error when it fails fetching the data

      - CepEvents.CepFetchFinish
        With CEP data or error, when the request is finished (with error or not).
 */

export const cepFetcherInstallEvent = new CustomEvent(CepEvents.InstallHandler, {
    detail: {
        handlerName: "cepFetcher",
        installer: cepFetcherInstaller,
    },
});

function cepFetcherInstaller({
    quickDispatchEvent,
    quickAddEventListener,
    getCepURL,
}: HandlerParams) {
    return quickAddEventListener(CepEvents.ValidCepInput, (cep: string) => {
        const cepURL = getCepURL(cep);
        quickDispatchEvent(CepEvents.CepFetchStart, cepURL);

        fetchCepData(cepURL)
            .then(
                (response) => quickDispatchEvent(CepEvents.CepFetchSuccess, response),
                (error) => quickDispatchEvent(CepEvents.CepFetchError, error)
            )
            .then((value) => quickDispatchEvent(CepEvents.CepFetchFinish, value));
    });
}

const fetchCepData = (url: string): Promise<CepDataType> =>
    fetch(url).then((response) => {
        if (response.status >= 200 && response.status < 300) {
            return response.json();
        } else {
            var error: any = new Error(response.statusText || response.status.toString());
            error.response = response;
            return Promise.reject(error);
        }
    });
