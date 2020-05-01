import {cepCleanerInstallEvent} from "./cepCleaner";
import {cepValidatorInstallEvent} from "./cepValidator";
import {cepFetcherInstallEvent} from "./cepFetcher";
import {cepLoadingIndicatorInstallEvent} from "./cepLoadingIndicator";
import {cepFieldsLockerInstallEvent} from "./cepFieldsLocker";
import {cepFieldsFillerInstallEvent} from "./cepFieldsFiller";
import {cepFieldsAutoFocusInstallEvent} from "./cepFieldsAutoFocus";

export const defaultInstallerEvents: Array<CustomEvent> = [
    cepCleanerInstallEvent,
    cepValidatorInstallEvent,
    cepFetcherInstallEvent,
    cepLoadingIndicatorInstallEvent,
    cepFieldsLockerInstallEvent,
    cepFieldsFillerInstallEvent,
    cepFieldsAutoFocusInstallEvent,
];
