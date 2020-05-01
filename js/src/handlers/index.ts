import {cepCleanerInstallEvent} from "./cepCleaner";
import {cepValidatorInstallEvent} from "./cepValidator";
import {CepFetcherInstallEvent} from "./cepFetcher";
import {cepLoadingIndicatorInstallEvent} from "./cepLoadingIndicator";
import {CepFieldsFillerInstallEvent} from "./cepFieldsFiller";
import {cepFieldsAutoFocusInstallEvent} from "./cepFieldsAutoFocus";

export const defaultInstallerEvents: Array<CustomEvent> = [
    cepCleanerInstallEvent,
    cepValidatorInstallEvent,
    CepFetcherInstallEvent,
    cepLoadingIndicatorInstallEvent,
    CepFieldsFillerInstallEvent,
    cepFieldsAutoFocusInstallEvent,
];
