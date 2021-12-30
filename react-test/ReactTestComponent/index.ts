import React = require("react");
import ReactDOM = require("react-dom");
import {IInputs, IOutputs} from "./generated/ManifestTypes";
import ReactSampleTextBox, { IProps } from "./ReactSampleTestBox";

export class ReactTestComponent implements ComponentFramework.StandardControl<IInputs, IOutputs> {

	private _value: string | undefined;
	private _Items: ComponentFramework.PropertyTypes.DataSet;
	private _notifyOutputChanged:() => void;
	private _container: HTMLDivElement;
	private _context: ComponentFramework.Context<IInputs>;
	private props: IProps = { value : "", Items: null, onChange: this.notifyChange.bind(this) };

	public refreshData(evt: Event) : void
	{
		this._notifyOutputChanged();
	}

	/**
	 * Empty constructor.
	 */
	constructor()
	{

	}

	/**
	 * Used to initialize the control instance. Controls can kick off remote server calls and other initialization actions here.
	 * Data-set values are not initialized here, use updateView.
	 * @param context The entire property bag available to control via Context Object; It contains values as set up by the customizer mapped to property names defined in the manifest, as well as utility functions.
	 * @param notifyOutputChanged A callback method to alert the framework that the control has new outputs ready to be retrieved asynchronously.
	 * @param state A piece of data that persists in one session for a single user. Can be set at any point in a controls life cycle by calling 'setControlState' in the Mode interface.
	 * @param container If a control is marked control-type='standard', it will receive an empty div element within which it can render its content.
	 */
	public init(context: ComponentFramework.Context<IInputs>, notifyOutputChanged: () => void, state: ComponentFramework.Dictionary, container:HTMLDivElement): void
	{
		// Add control initialization code
		this._notifyOutputChanged = notifyOutputChanged;
		this._container = document.createElement("div");
		this.props.value = context.parameters.selectedId.raw || "";
		this.props.Items = context.parameters.Items;

		container.appendChild(this._container);
	}

	notifyChange(value:string, Items: ComponentFramework.PropertyTypes.DataSet) {
		this._value = value;
		this._Items = Items;
		this._notifyOutputChanged();
	}


	/**
	 * Called when any value in the property bag has changed. This includes field values, data-sets, global values such as container height and width, offline status, control metadata values such as label, visible, etc.
	 * @param context The entire property bag available to control via Context Object; It contains values as set up by the customizer mapped to names defined in the manifest, as well as utility functions
	 */
	public updateView(context: ComponentFramework.Context<IInputs>): void
	{
		// Add code to update control view
		this._value = context.parameters.selectedId.raw?.valueOf();
		this._Items = context.parameters.Items;
		this.props.value = this._value;
		this.props.Items = this._Items;
		ReactDOM.render(
			React.createElement(ReactSampleTextBox, this.props)
			, this._container
		);
	}


	/**
	 * It is called by the framework prior to a control receiving new data.
	 * @returns an object based on nomenclature defined in manifest, expecting object[s] for property marked as “bound” or “output”
	 */
	public getOutputs(): IOutputs
	{
		return {
			selectedId : this._value
		};
	}

	/**
	 * Called when the control is to be removed from the DOM tree. Controls should use this call for cleanup.
	 * i.e. cancelling any pending remote calls, removing listeners, etc.
	 */
	public destroy(): void
	{
		// Add code to cleanup control if necessary
		ReactDOM.unmountComponentAtNode(this._container);
	}
}