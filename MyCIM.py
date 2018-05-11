import CIM15.IEC61970.Core as Core
import CIM15.IEC61970.Wires as Wires
import CIM15.IEC61970.Generation.Production as Production
import CIM15.IEC61970.Equivalents as Equivalents


# SOME CLASSES ARE NOT PRESENT IN CIM15 

class EnergySource:
    def __init__(self):
        self._Terminals = []
        
class PetersenCoil:
    def __init__(self):
        self._Terminals = []  
        
        


## registry of classes
    
registry = {
        "Substation":Core.Substation, 
        "BaseVoltage":Core.BaseVoltage,
        "VoltageLevel":Core.VoltageLevel,
        "SynchronousMachine":Wires.SynchronousMachine,
        "RegulatingControl":Wires.RegulatingControl,
        "PowerTransformer":Wires.PowerTransformer,
        "EnergyConsumer":Wires.EnergyConsumer,
        "PowerTransformerEnd":Wires.PowerTransformerEnd,
        "Breaker":Wires.Breaker,
        "RatioTapChanger":Wires.RatioTapChanger,
        "Region":Core.SubGeographicalRegion,
        "EquipmentContainer":Core.EquipmentContainer,
        "GeneratingUnit":Production.GeneratingUnit,
        "ACLineSegment":Wires.ACLineSegment,    
        "BusbarSection":Wires.BusbarSection,
        "ConnectivityNode":Core.ConnectivityNode,
        "Terminal":Core.Terminal,
        "Line":Wires.Line,
        "ConnectivityNodeContainer":Core.ConnectivityNodeContainer,
        "LinearShuntCompensator":Wires.ShuntCompensator, # Note: should be LinearShuntCompensator
        "RatioTapChanger":Wires.RatioTapChanger,
        "PhaseTapChangerAsymetrical":Wires.PhaseTapChangerAsymetrical,
        "EnergySource":EnergySource, # Note: EnergySource not present in CIM15
        "EquivalentInjection":Equivalents.EquivalentInjection,
        "PetersenCoil":PetersenCoil
        }
        
        
## remaining objects ##         
# CurrentLimit
# CurveData
# LoadResponseCharacteristics
# OperationalLimitSet
# OperationalLimitType
# ReactiveCapabilityCurve
# TapChangerControl

        
# The fields which should be parsed and entered into data base. The lists are as follows:
object_fields = {
            "Substation":[],
            "BaseVoltage":['nominalVoltage'],
            "VoltageLevel":[],
            "GeneratingUnit":['maxOperatingP','minOperatingP'],
            "SynchronousMachine":['ratedS','qPercent','maxQ','minQ','ratedU','ratedPowerFactor','p','q'],
            "RegulatingControl":['targetValue'],
            "PowerTransformer":[],
            "EnergyConsumer":['p','q'],
            "PowerTransformerEnd":['r','x','b','g'],
            "Breaker":['open'],
            "RatioTapChanger":['step'],
            "Region":[],
            "EquipmentContainer":[],
            "ACLineSegment":['r','x','bch','gch','length','r0','x0','b0ch','g0ch'],
            "BusbarSection":[],
            "ConnectivityNode":[],
            "Terminal":[],
            "Line":[],
            "ConnectivityNodeContainer":[],
            "LinearShuntCompensator":['nomU','bPerSection','gPerSection','sections'],
            "RatioTapChanger":['neutralU','lowStep','highStep','neutralStep','normalStep','step','ltcFlag'],
            "PhaseTapChangerAsymetrical":[],
            "EnergySource":['r','x','activePower','reactivePower'],
            "EquivalentInjection":['p','q'],
            "PetersenCoil":['r','xGroundnominal','xGroundMax','xGroundMin','positionCurrent','offsetCurrent','nominalU']
        }
        
object_foreign_keys = {"Substation":['Region'],
                       "BaseVoltage":[],
                       "VoltageLevel":['BaseVoltage','Substation'],
                       "GeneratingUnit":['EquipmentContainer'],
                       "SynchronousMachine":['GeneratingUnit','RegulatingControl','EquipmentContainer'],
                       "RegulatingControl":[],
                       "PowerTransformer":['EquipmentContainer'],
                       "EnergyConsumer":['EquipmentContainer','BaseVoltage'],
                       "PowerTransformerEnd":['PowerTransformer','BaseVoltage','Terminal'],
                       "Breaker":['EquipmentContainer','BaseVoltage'],
                       "RatioTapChanger":[],
                       "Region":[],
                       "EquipmentContainer":[],
                       "ACLineSegment":['EquipmentContainer','BaseVoltage'],
                       "BusbarSection":['EquipmentContainer'],
                       "ConnectivityNode":['ConnectivityNodeContainer'],
                       "Terminal":['ConductingEquipment','ConnectivityNode'],
                       "Line":['Region'],
                       "ConnectivityNodeContainer":[],
                       "LinearShuntCompensator":['EquipmentContainer'],
                       "RatioTapChanger":['TransformerEnd'],
                       "PhaseTapChangerAsymetrical":['TransformerEnd'],
                       "EnergySource":['EquipmentContainer'],
                       "EquivalentInjection":['BaseVoltage'],
                       "PetersenCoil":['EquipmentContainer']
                       }

    