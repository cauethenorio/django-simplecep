import {HandlerParams} from "./types";
import {installHandlers} from "./install-handlers";

const getById = (id: string): HTMLElement | null => document.getElementById(id);

describe("installHandlers", () => {
    it("should execute each handler once", () => {
        const fieldDataMock: any = jest.fn();
        const handler1Mock = jest.fn();
        const handler2Mock = jest.fn();

        installHandlers(fieldDataMock, [handler1Mock, handler2Mock]);

        expect(handler1Mock.mock.calls.length).toBe(1);
        expect(handler2Mock.mock.calls.length).toBe(1);
        expect(handler1Mock.mock.calls[0]).toEqual(handler2Mock.mock.calls[0]);
    });

    it("should correctly listen/dispatch DOM node events", () => {
        document.body.innerHTML = '<input type="text" id="field">';
        const eventData = {my: "data"};

        const listenerMock = jest.fn();

        const handler = ({dispatch, addListener}: HandlerParams) => {
            addListener("test-event", listenerMock);
            dispatch("test-event", eventData);
        };

        installHandlers(
            {
                cepField: document.getElementById("field") as HTMLInputElement,
                baseCepURL: "",
                dataFields: []
            },
            [handler]
        );

        expect(listenerMock.mock.calls.length).toBe(1);
        expect(listenerMock.mock.calls[0][0]).toBe(eventData);
    });

    it("should generate CEP endpoint URL based on the provided baseCepURL", () => {
        installHandlers(
            {
                cepField: null,
                baseCepURL: "/my-custom-cep-endpoint/00000000",
                dataFields: []
            },
            [
                ({getCepURL}) => {
                    expect(getCepURL("12345678")).toBe(
                        "/my-custom-cep-endpoint/12345678"
                    );
                }
            ]
        );
    });

    it("should create a map of CEP data fields when getDataFields is called", () => {
        document.body.innerHTML = `
            <input type="text" id="field1" class="city">
            <div id="div1">state</div>
            <span id="span1">district</span>
        `;

        installHandlers(
            {
                cepField: null,
                baseCepURL: "",
                dataFields: [
                    {type: "state", selector: "#div1"},
                    {type: "city", selector: ".city"},
                    {type: "district", selector: "#span1"},
                    {type: "address", selector: "#non-existent"}
                ]
            },
            [
                ({getDataFields}) => {
                    expect(getDataFields()).toEqual([
                        {type: "state", els: [getById("div1")]},
                        {type: "city", els: [getById("field1")]},
                        {type: "district", els: [getById("span1")]},
                        {type: "address", els: []}
                    ]);
                }
            ]
        );
    });
});
