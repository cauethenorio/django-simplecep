import {CepEvents} from "../types";
import {installHandlers} from "../install-handlers";
import {cepInputHandler} from "./cep-input";

function setupHandler(
    value: string,
    invalidCepListener: (e: CustomEvent<string>) => void,
    validCepListener: (e: CustomEvent<string>) => void
) {
    var node = document.createElement("input");
    node.setAttribute("type", "text");
    node.value = value;

    installHandlers(
        {
            cepField: node,
            baseCepURL: "",
            dataFields: []
        },
        [cepInputHandler]
    );

    node.addEventListener(CepEvents.InvalidCepInput, invalidCepListener);
    node.addEventListener(CepEvents.ValidCepInput, validCepListener);

    node.dispatchEvent(
        new Event("input", {
            bubbles: true,
            cancelable: true
        })
    );

    return {
        invalidCepListener,
        validCepListener
    };
}

describe("cepInputHandler", () => {
    it.each(["000000", "", "1234567a", "aaaa", "12345_678", "111112222"])(
        'should trigger CepEvents.InvalidCepInput for invalid CEP input "%s"',
        (value: string) => {
            const listeners = setupHandler(
                value,
                jest.fn((e: CustomEvent<string>) => expect(e.detail).toBe(value)),
                jest.fn()
            );

            expect(listeners.invalidCepListener).toBeCalled();
            expect(listeners.validCepListener).not.toBeCalled();
        }
    );

    it.each([
        ["12345678", "12345678"],
        ["11111 111", "11111111"],
        ["18170-000", "18170000"]
    ])(
        'should trigger CepEvents.ValidCepInput for valid CEP input "%s"',
        (value: string, formattedCep: string) => {
            const listeners = setupHandler(
                value,
                jest.fn(),
                jest.fn((e: CustomEvent<string>) => expect(e.detail).toBe(formattedCep))
            );

            expect(listeners.validCepListener).toBeCalled();
            expect(listeners.invalidCepListener).not.toBeCalled();
        }
    );
});
