import {CepEvents, DataFieldType, HandlerParams} from "../types";

type CepDataType = {[key in DataFieldType]: string | null};

const fetchCepData = (url: string): Promise<CepDataType> =>
    fetch(url).then(response => {
        if (response.status >= 200 && response.status < 300) {
            return response.json();
        } else {
            var error: any = new Error(
                response.statusText || response.status.toString()
            );
            error.response = response;
            return Promise.reject(error);
        }
    });

export function fetchCepHandler({dispatch, addListener, getCepURL}: HandlerParams) {
    let lastRequestedCep: string;

    addListener(CepEvents.ValidCepInput, (cep: any) => {
        const cepURL = getCepURL(cep as string);
        lastRequestedCep = cep;

        fetchCepData(cepURL)
            .then(
                response =>
                    dispatch(
                        lastRequestedCep === cep
                            ? CepEvents.CepFetchSuccess
                            : CepEvents.CepFetchIgnore,
                        response
                    ),
                error => dispatch(CepEvents.CepFetchError, error)
            )
            .then(value => dispatch(CepEvents.CepFetchFinish, value));

        dispatch(CepEvents.CepFetchStart, cepURL);
    });
}
