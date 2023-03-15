# Deploy SAI PTF Test Topology With SONiC-MGMT
*In this article, you will get to know how to use the sonic-mgmt docker to set up the topology for sai testing.*

- [Deploy SAI PTF Test Topology With SONiC-MGMT](#deploy-sai-ptf-test-topology-with-sonic-mgmt)
- [reference](#reference)

> **Those commands need to be run within a sonic-mgmt docker, or you need to run them within a similar environment.** 

For how to setup the sonic-mgmt docker please refer to [setup-sonic-mgmt-docker](https://github.com/Azure/sonic-mgmt/blob/master/docs/testbed/README.testbed.VsSetup.md#setup-sonic-mgmt-docker)


1. install the sonic image in the DUT(device under test)

   for example
   ```
   SONiC Software Version: SONiC.20220701.01
   ```
2. remove the topology for the current testbed (Optional)
   
   For SAI-PTF testing, cause it uses PTF32 topology, which is different from other [SONiC Logical topologies](https://github.com/sonic-net/sonic-mgmt/blob/master/docs/testbed/README.testbed.Overview.md#logical-topologies) if you already deployed some T0, T1 topology, you need to remove them at first.
   
   In SONiC-mgmt docker
      
   ```
   cd /data/<sonic-mgmt-clone>/ansible
   ./testbed-cli.sh remove-topo str-s6000-acs-10 password.txt
   ```

3. Config PTF 32 topology deployment

   In order to deploy the PTF 32 environment, we need to change the topology to 'ptf32' by modifying the testbed.yml

   For example, if we want to use the config `str-s6000-acs-10`, then we need to change it
   > Note: Below environment is just for example, please use your local physical environment for actual testing.  
   ```git
    - conf-name: vms11-t0-s6000
      group-name: vms11-4
   -  topo: t0
   +  topo: ptf32                         # <-- change to ptf32 topo
      ptf_image_name: docker-ptf-saiv2    # <-- ptf dockre image name
      ptf: vms11-4                        # <-- docker instance name 
      ptf_ip: 10.64.246.83/23             # <-- docker-ptf-saiv2 IP
      ptf_ipv6:
      server: server_1
      dut:
        - str-s6000-acs-10
   ```

   > **for the topo, if it ends with 64, then the topo should be ptf64, please change it according to the actual device port.**

   > Make sure you push docker docker-ptf-saiv2 correctly [Setup the testbed by sonic-mgmt](SAI-PTFv2Overview.md#setup-the-testbed-by-sonic-mgmt)


   > Note: By default, we use PTF32 topology for SAI PTF testing. With PTF32 topology, it will use 32 ports, it needs to test against more ports, like 64 ports, please use the PTF64 topology or other customized configuration.

   > Compared with other [SONiC Logical topologies](https://github.com/sonic-net/sonic-mgmt/blob/master/docs/testbed/README.testbed.Overview.md#logical-topologies), SAI-PTFv2 is simpler, it only gets connected from PTF to DUT. 

   > For more detail about the SONiC testbed topology please refer to [sonic testbed overview](https://github.com/sonic-net/sonic-mgmt/blob/master/docs/testbed/README.testbed.Overview.md).

4. deploy the new topology
   In sonic-mgmt docker
   ```
   cd /data/<sonic-mgmt-clone>/ansible
   ./testbed-cli.sh -t testbed.yaml add-topo <conf-name> password.txt
   # password.txt can not be an empty file, you can input `123` in it.
   ```
   For example, for the test bed config `vms11-t0-s6000`, it should be
   ```
   /data/<sonic-mgmt-clone>/ansible/testbed-cli.sh -t testbed.yaml add-topo vms11-t0-s6000 password.txt
   ```

   > **Note: vms11-t0-s6000 is a sample testbed name, please use the actual name as needed.**

# reference

For understanding the topology concept, please refer to the doc
[Topologies](https://github.com/Azure/sonic-mgmt/blob/master/docs/testbed/README.testbed.Topology.md)

For how to find the topology info and the related device please refer to the doc
[Example of Testbed Configuration](https://github.com/Azure/sonic-mgmt/blob/master/docs/testbed/README.testbed.Example.Config.md)

For the example to set up the testbed with the related command please refer to 
- Contains how to build the related PTF, sonic-mgmt docker
[Testbed Setup](https://github.com/Azure/sonic-mgmt/blob/master/docs/testbed/README.testbed.Setup.md)
- More concentrate on a virtual environment with KVM and Docker
[KVM Testbed Setup](https://github.com/Azure/sonic-mgmt/blob/master/docs/testbed/README.testbed.VsSetup.md)