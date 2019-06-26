import {scanSimpleCepFields} from "./scanner";

describe("scanSimpleCepFields", () => {
    test("should find a single field and extract its data", () => {
        document.body.innerHTML = `
        <p>
            <label for="crazy_field_id">Cep:</label>
            <input
                type="text"
                name="cep"
                maxlength="9"
                inputmode="decimal"
                required=""
                data-simplecep-autocomplete=""
                data-simplecep-get-cep-url="/my-cep-route/00000000/"
                data-simplecep-state-field-id="id_estado"
                data-simplecep-random-field-id="id_estado"
                id="crazy_field_id"
            >
        </p>
        <p>
            <label for="id_estado">Estado:</label>
            <input type="text" name="estado" required="" id="id_estado">
        </p>
    `;

        expect(scanSimpleCepFields()).toEqual([
            {
                cepField: document.getElementById("crazy_field_id"),
                getCepURL: "/my-cep-route/00000000/",
                fieldsIds: {state: "id_estado"}
            }
        ]);
    });

    test("should find multiple fields and extract their data", () => {
        document.body.innerHTML = `
        <p><div>
            <input
                type="text"
                name="cep"
                maxlength="9"
                inputmode="decimal"
                required=""
                data-simplecep-autocomplete=""
                data-simplecep-get-cep-url="/my-cep-route/00000000/"
                data-simplecep-state-field-id="id_estado"
                data-simplecep-random-field-id="id_estado"
                id="first_one"
            >
        </div></p>
        <p><div>
            <input
                type="text"
                data-simplecep-autocomplete
                data-simplecep-get-cep-url="/another-cep-route/00000000/"
                data-simplecep-state-field-id="statez"
                data-simplecep-city-field-id="cityz"
                data-simplecep-district-field-id="districtz"
                data-simplecep-address-field-id="addressz"
                data-simplecep--field-id="ignore-me"
                id="2nd_field"
            >
        </div></p>`;

        expect(scanSimpleCepFields()).toEqual([
            {
                cepField: document.getElementById("first_one"),
                getCepURL: "/my-cep-route/00000000/",
                fieldsIds: {state: "id_estado"}
            },
            {
                cepField: document.getElementById("2nd_field"),
                getCepURL: "/another-cep-route/00000000/",
                fieldsIds: {
                    state: "statez",
                    city: "cityz",
                    district: "districtz",
                    address: "addressz"
                }
            }
        ]);
    });
});
