import {HandlerParams} from "../types";

import {cepInputHandler} from "./cep-input";
import {fetchCepHandler} from "./fetch-cep";
import {cepMaskHandler} from "./cep-mask";
import {fillFields} from "./fill-fields";
import {loadingIndicatorHandler} from "./loading-indicator";

export const defaultHandlers: Array<(params: HandlerParams) => void> = [
    cepInputHandler,
    fetchCepHandler,
    cepMaskHandler,
    fillFields,
    loadingIndicatorHandler
];
