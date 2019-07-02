import {querySimplecepAutofillFields} from "./fields-finder";

describe("querySimplecepAutofillFields", () => {
    it("should find a single field and extract its data", () => {
        document.body.innerHTML = `
        <p>
            <label for="crazy_field_id">Cep:</label>
            <input
                type="text"
                name="cep"
                maxlength="9"
                inputmode="decimal"
                required=""
                data-simplecep-autofill="{&quot;baseCepURL&quot;: &quot;/my-cep-route/00000000/&quot;, &quot;dataFields&quot;: [{&quot;selector&quot;: &quot;#my_custom_id&quot;, &quot;type&quot;: &quot;address&quot;}]}"
                id="crazy_field_id"
            >
        </p>
        <p>
            <label for="id_estado">Estado:</label>
            <input type="text" name="estado" required="" id="id_estado">
        </p>
    `;

        expect(querySimplecepAutofillFields()).toEqual([
            {
                cepField: document.getElementById("crazy_field_id"),
                baseCepURL: "/my-cep-route/00000000/",
                dataFields: [{type: "address", selector: "#my_custom_id"}]
            }
        ]);
    });

    it("should find multiple fields and extract their data", () => {
        document.body.innerHTML = `
        <p><div>
            <input
                type="text"
                name="cep"
                maxlength="9"
                inputmode="decimal"
                required=""
                data-simplecep-autofill="{&quot;baseCepURL&quot;: &quot;/my-cep-route/00000000/&quot;, &quot;dataFields&quot;: [{&quot;selector&quot;: &quot;#id_estado&quot;, &quot;type&quot;: &quot;state&quot;}]}"
                id="first_one"
            >
        </div></p>
        <p><div>
            <input
                type="text"
                data-simplecep-autofill="{&quot;baseCepURL&quot;: &quot;/another-cep-route/00000000/&quot;, &quot;dataFields&quot;: [{&quot;selector&quot;: &quot;#id_statez&quot;, &quot;type&quot;: &quot;state&quot;}, {&quot;selector&quot;: &quot;#id_cityz&quot;, &quot;type&quot;: &quot;city&quot;}, {&quot;selector&quot;: &quot;#id_districtz&quot;, &quot;type&quot;: &quot;district&quot;}, {&quot;selector&quot;: &quot;#id_addressz&quot;, &quot;type&quot;: &quot;address&quot;}]}"
                id="2nd_field"
            >
        </div></p>`;

        expect(querySimplecepAutofillFields()).toEqual([
            {
                cepField: document.getElementById("first_one"),
                baseCepURL: "/my-cep-route/00000000/",
                dataFields: [{type: "state", selector: "#id_estado"}]
            },
            {
                cepField: document.getElementById("2nd_field"),
                baseCepURL: "/another-cep-route/00000000/",
                dataFields: [
                    {type: "state", selector: "#id_statez"},
                    {type: "city", selector: "#id_cityz"},
                    {type: "district", selector: "#id_districtz"},
                    {type: "address", selector: "#id_addressz"}
                ]
            }
        ]);
    });

    it("should remove the node attribute after getting the data", () => {
        document.body.innerHTML = `<input data-simplecep-autofill="{&quot;key&quot;: &quot;value&quot;}">`;
        expect(querySimplecepAutofillFields()).toHaveLength(1);
        expect(querySimplecepAutofillFields()).toHaveLength(0);
    });
});
