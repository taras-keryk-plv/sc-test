Override VRF
-------------------------------------------------------------------------------
 Title       | SAI Override VRF
-------------|-----------------------------------------------------------------
 Authors     | Jai Kumar, Broadcom Inc.
 Status      | In review
 Type        | Standards track
 Created     | 02/18/2021
 SAI-Version | 1.7.2
 
 
-------------------------------------------------------------------------------

This spec talks about the override VRF usecase.

SAI pipleine define L3 lookup block as an abstracted stage where route lookup is abstracted as a single operation. 
SAI pipeline do not specify how many parallel L3 lookups a device can/may support.

Typically devices support multiple parallel L3 lookup to provide policy based forwarding.
Following usecase 1 is already covered in SAI spec. This spec adds support for usecase 2 and 3.

New switch level default override VRF is introduced. 
```
    /**
     * @brief Default SAI Override Virtual Router ID
     *
     * Must return #SAI_STATUS_OBJECT_IN_USE when try to delete this VR ID.
     *
     * @type sai_object_id_t
     * @flags READ_ONLY
     * @objects SAI_OBJECT_TYPE_VIRTUAL_ROUTER
     * @default internal
     */
    SAI_SWITCH_ATTR_DEFAULT_OVERRIDE_VIRTUAL_ROUTER_ID,
```


### Usecase 1: VRF Fallback
In this case 2 parrallel lookups are performed
```
Lookup 1: RIF/ACL -> VRF -> [VRF, DIP] -> R1
Lookup 2: Switch -> Deafault_VRF -> [Default_VRF, DIP] -> R2

if (R1)
    use R1;
elif (R2)
   use R2;
else
   MISS action;
```



### Usecase 2: Override VRF
In this case 2 parallel lookups are performed
```
Lookup 1: Switch -> Override_VRF -> [Override_VRF, DIP] -> R1
Lookup 2: RIF/ACL -> VRF -> [VRF, DIP] -> R2

if (R1)
    use R1;
elif (R2)
   use R2;
else
   MISS action;
```

### Usecase 3: Override VRF and VRF Fallback
In this case 3 parallel lookups are performed
```
Lookup 1: Switch -> Override_VRF -> [Override_VRF, DIP] -> R1
Lookup 2: RIF/ACL -> VRF -> [VRF, DIP] -> R2
Lookup 2: Switch -> Deafault_VRF -> [Default_VRF, DIP] -> R3

if (R1)
    use R1;
elif (R2)
   use R2;
elif (R3)
   use R3;
else
   MISS action;
```

Example WorkFlow:
Since SAI_SWITCH_ATTR_DEFAULT_OVERRIDE_VIRTUAL_ROUTER_ID is a READ only attribute, SAI adapter creates a VRF object (virtual_router) during init. This object is emtpy and is returned when application quries for the override VRF.
Application MUST provide this VRF in the route update API.
```
typedef struct _sai_route_entry_t
{
    /**
     * @brief Switch ID
     *
     * @objects SAI_OBJECT_TYPE_SWITCH
     */
    sai_object_id_t switch_id;

    /**
     * @brief Virtual Router ID
     *
     * @objects SAI_OBJECT_TYPE_VIRTUAL_ROUTER
     */
    sai_object_id_t vr_id;

    /**
     * @brief IP Prefix Destination
     */
    sai_ip_prefix_t destination;

} sai_route_entry_t;

```

> SAI adapter should return error if platform do not support SAI_SWITCH_ATTR_DEFAULT_OVERRIDE_VIRTUAL_ROUTER_ID switch attribute
