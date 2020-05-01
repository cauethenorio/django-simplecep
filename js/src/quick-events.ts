import {HandlerParams} from "./types";

const createDispatcher = (el: HTMLElement): HandlerParams["quickDispatchEvent"] => (
    eventName: string,
    detail: any
) => {
    const event = new CustomEvent(eventName, {detail});
    console.log(`Dispatching ${eventName}.`);
    el.dispatchEvent(event);
};

const createListenerFactory = (el: HTMLElement): HandlerParams["quickAddEventListener"] => <D>(
    eventName: string,
    listener: (detail: D, e: CustomEvent<D>) => void
) => {
    const listenerWrapper = (e: CustomEvent<D>) => listener(e.detail, e as CustomEvent<D>);

    el.addEventListener(eventName, listenerWrapper);
    console.log(`Event listener registered for '${eventName}'.`);
    return () => el.removeEventListener(eventName, listenerWrapper);
};

export function createQuickEventsFuncsFor(el: HTMLElement) {
    return {
        quickAddEventListener: createListenerFactory(el),
        quickDispatchEvent: createDispatcher(el),
    };
}
