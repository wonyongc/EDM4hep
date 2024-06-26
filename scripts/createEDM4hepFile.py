# Description: Create a file with EDM4hep data using the EDM4hep python bindings
# The purpose of the script is to use all the classes of the EDM4hep library
# to create a file with dummy data.
import podio
import edm4hep
from itertools import count
import argparse
import sys

frames = 10  # How many frames or events will be written
vectorsize = 5  # For vector members, each vector member will have this size
counter = count()  # next(counter) will return 0, 1, 2, ...
# used to generate the dummy data
output_file = "output.root"

parser = argparse.ArgumentParser(description="Create a file with EDM4hep data")
parser.add_argument(
    "--use-pre1", action="store_true", help="Use a pre 1.0 version of EDM4hep"
)
parser.add_argument(
    "--rntuple", action="store_true", help="Use a ROOT ntuple instead of EDM4hep"
)
args = parser.parse_args()

if args.rntuple:
    try:
        writer = podio.root_io.RNTupleWriter(output_file)
    except AttributeError:
        print("The RNTuple writer from podio is not available but was requested")
        sys.exit(1)


writer = podio.root_io.Writer(output_file)

for i in range(frames):
    print(f"Writing frame {i}")
    frame = podio.Frame()

    header = edm4hep.EventHeaderCollection()
    h = header.create()
    h.setEventNumber(next(counter))
    h.setRunNumber(next(counter))
    h.setTimeStamp(next(counter))
    h.setWeight(1.0)
    if not args.use_pre1:
        for j in range(vectorsize):
            h.addToWeights(next(counter))
    frame.put(header, "EventHeader")

    particles = edm4hep.MCParticleCollection()
    parent_particle = particles.create()
    parent_particle.setPDG(next(counter))
    parent_particle.setGeneratorStatus(next(counter))
    parent_particle.setSimulatorStatus(next(counter))
    parent_particle.setCharge(next(counter))
    parent_particle.setTime(next(counter))
    parent_particle.setMass(next(counter))
    parent_particle.setVertex(
        edm4hep.Vector3d(next(counter), next(counter), next(counter))
    )
    parent_particle.setEndpoint(
        edm4hep.Vector3d(next(counter), next(counter), next(counter))
    )
    if not args.use_pre1:
        parent_particle.setMomentum(
            edm4hep.Vector3d(next(counter), next(counter), next(counter))
        )
        parent_particle.setMomentumAtEndpoint(
            edm4hep.Vector3d(next(counter), next(counter), next(counter))
        )
    else:
        parent_particle.setMomentum(
            edm4hep.Vector3f(next(counter), next(counter), next(counter))
        )
        parent_particle.setMomentumAtEndpoint(
            edm4hep.Vector3f(next(counter), next(counter), next(counter))
        )
    parent_particle.setSpin(
        edm4hep.Vector3f(next(counter), next(counter), next(counter))
    )
    parent_particle.setColorFlow(edm4hep.Vector2i(next(counter), next(counter)))

    daughter_particle = particles.create()
    daughter_particle.setPDG(next(counter))
    daughter_particle.setGeneratorStatus(next(counter))
    daughter_particle.setSimulatorStatus(next(counter))
    daughter_particle.setCharge(next(counter))
    daughter_particle.setTime(next(counter))
    daughter_particle.setMass(next(counter))
    daughter_particle.setVertex(
        edm4hep.Vector3d(next(counter), next(counter), next(counter))
    )
    daughter_particle.setEndpoint(
        edm4hep.Vector3d(next(counter), next(counter), next(counter))
    )
    if not args.use_pre1:
        daughter_particle.setMomentum(
            edm4hep.Vector3d(next(counter), next(counter), next(counter))
        )
        daughter_particle.setMomentumAtEndpoint(
            edm4hep.Vector3d(next(counter), next(counter), next(counter))
        )
    else:
        daughter_particle.setMomentum(
            edm4hep.Vector3f(next(counter), next(counter), next(counter))
        )
        daughter_particle.setMomentumAtEndpoint(
            edm4hep.Vector3f(next(counter), next(counter), next(counter))
        )
    daughter_particle.setSpin(
        edm4hep.Vector3f(next(counter), next(counter), next(counter))
    )
    daughter_particle.setColorFlow(edm4hep.Vector2i(next(counter), next(counter)))

    parent_particle.addToDaughters(daughter_particle)
    daughter_particle.addToParents(parent_particle)
    frame.put(particles, "MCParticleCollection")

    hits = edm4hep.SimTrackerHitCollection()
    hit = hits.create()
    hit.setCellID(next(counter))
    hit.setEDep(next(counter))
    hit.setTime(next(counter))
    hit.setPathLength(next(counter))
    hit.setQuality(next(counter))
    hit.setPosition(edm4hep.Vector3d(next(counter), next(counter), next(counter)))
    hit.setMomentum(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    hit.setParticle(daughter_particle)
    simtracker_hit = hit
    frame.put(hits, "SimTrackerHitCollection")

    hits = edm4hep.CaloHitContributionCollection()
    hit = hits.create()
    hit.setPDG(next(counter))
    hit.setEnergy(next(counter))
    hit.setTime(next(counter))
    hit.setStepPosition(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    hit.setParticle(daughter_particle)
    calohit = hit
    frame.put(hits, "CaloHitContributionCollection")

    hits = edm4hep.SimCalorimeterHitCollection()
    hit = hits.create()
    hit.setCellID(next(counter))
    hit.setEnergy(next(counter))
    hit.setPosition(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    hit.addToContributions(calohit)
    simcalo_hit = hit
    frame.put(hits, "SimCalorimeterHitCollection")

    hits = edm4hep.RawCalorimeterHitCollection()
    hit = hits.create()
    hit.setCellID(next(counter))
    hit.setAmplitude(next(counter))
    hit.setTimeStamp(next(counter))
    frame.put(hits, "RawCalorimeterHitCollection")

    hits = edm4hep.CalorimeterHitCollection()
    hit = hits.create()
    hit.setCellID(next(counter))
    hit.setEnergy(next(counter))
    hit.setEnergyError(next(counter))
    hit.setTime(next(counter))
    hit.setPosition(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    hit.setType(next(counter))
    calo_hit = hit
    frame.put(hits, "CalorimeterHitCollection")

    pids = edm4hep.ParticleIDCollection()
    pid = pids.create()
    pid.setType(next(counter))
    pid.setPDG(next(counter))
    pid.setAlgorithmType(next(counter))
    pid.setLikelihood(next(counter))
    for j in range(vectorsize):
        pid.addToParameters(next(counter))
    frame.put(pids, "ParticleIDCollection")

    clusters = edm4hep.ClusterCollection()
    cluster = clusters.create()
    cluster.setType(next(counter))
    cluster.setEnergy(next(counter))
    cluster.setEnergyError(next(counter))
    cluster.setPosition(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    for j in range(6):
        cluster.setPositionError([next(counter) for _ in range(6)])
    cluster.setITheta(next(counter))
    cluster.setPhi(next(counter))
    cluster.setDirectionError(
        edm4hep.Vector3f(next(counter), next(counter), next(counter))
    )
    for j in range(vectorsize):
        cluster.addToShapeParameters(next(counter))
    for j in range(vectorsize):
        cluster.addToSubdetectorEnergies(next(counter))
    cluster.addToClusters(cluster)
    cluster.addToHits(calo_hit)
    if args.use_pre1:
        cluster.addToParticleIDs(pid)
    frame.put(clusters, "ClusterCollection")

    if args.use_pre1:
        hits = edm4hep.TrackerHitCollection()
    else:
        hits = edm4hep.TrackerHit3DCollection()
    hit = hits.create()
    hit.setCellID(next(counter))
    hit.setType(next(counter))
    hit.setQuality(next(counter))
    hit.setTime(next(counter))
    hit.setEDep(next(counter))
    hit.setEDepError(next(counter))
    hit.setPosition(edm4hep.Vector3d(next(counter), next(counter), next(counter)))
    hit.setCovMatrix([next(counter) for _ in range(6)])
    if args.use_pre1:
        for j in range(vectorsize):
            oid = edm4hep.ObjectID()
            oid.index = next(counter)
            oid.collectionID = next(counter)
            hit.addToRawHits(oid)
    tracker_hit = hit
    frame.put(hits, "TrackerHit3DCollection")

    hits = edm4hep.TrackerHitPlaneCollection()
    hit = hits.create()
    hit.setCellID(next(counter))
    hit.setType(next(counter))
    hit.setQuality(next(counter))
    hit.setTime(next(counter))
    hit.setEDep(next(counter))
    hit.setEDepError(next(counter))
    hit.setU(edm4hep.Vector2f(next(counter), next(counter)))
    hit.setV(edm4hep.Vector2f(next(counter), next(counter)))
    hit.setDu(next(counter))
    hit.setDv(next(counter))
    hit.setPosition(edm4hep.Vector3d(next(counter), next(counter), next(counter)))
    hit.setCovMatrix([next(counter) for _ in range(6)])
    if args.use_pre1:
        for j in range(vectorsize):
            oid = edm4hep.ObjectID()
            oid.index = next(counter)
            oid.collectionID = next(counter)
            hit.addToRawHits(oid)
    frame.put(hits, "TrackerHitPlaneCollection")

    series = edm4hep.RawTimeSeriesCollection()
    serie = series.create()
    serie.setCellID(next(counter))
    serie.setQuality(next(counter))
    serie.setTime(next(counter))
    serie.setCharge(next(counter))
    serie.setInterval(next(counter))
    for j in range(vectorsize):
        serie.addToAdcCounts(next(counter))
    frame.put(series, "RawTimeSeriesCollection")

    tracks = edm4hep.TrackCollection()
    track = tracks.create()
    track.setType(next(counter))
    track.setChi2(next(counter))
    track.setNdf(next(counter))
    track.setDEdx(next(counter))
    track.setDEdxError(next(counter))
    track.setRadiusOfInnermostHit(next(counter))
    for j in range(vectorsize):
        track.addToSubdetectorHitNumbers(next(counter))
    for j in range(vectorsize):
        state = edm4hep.TrackState()
        state.location = next(counter)
        state.d0 = next(counter)
        state.phi = next(counter)
        state.omega = next(counter)
        state.z0 = next(counter)
        state.tanLambda = next(counter)
        state.time = next(counter)
        state.referencePoint = edm4hep.Vector3f(
            next(counter), next(counter), next(counter)
        )
        state.CovMatrix = [next(counter) for _ in range(21)]
        track.addToTrackStates(state)
    track.addToTrackerHits(tracker_hit)
    track.addToTracks(track)
    frame.put(tracks, "TrackCollection")

    vertex = edm4hep.VertexCollection()
    v = vertex.create()
    v.setPrimary(next(counter))
    v.setChi2(next(counter))
    v.setProbability(next(counter))
    v.setPosition(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    v.setCovMatrix([next(counter) for _ in range(6)])
    v.setAlgorithmType(next(counter))
    for j in range(vectorsize):
        v.addToParameters(next(counter))
    frame.put(vertex, "VertexCollection")

    particles = edm4hep.ReconstructedParticleCollection()
    particle = particles.create()
    if args.use_pre1:
        particle.setType(next(counter))
    else:
        particle.setPDG(next(counter))
    particle.setEnergy(next(counter))
    particle.setMomentum(edm4hep.Vector3f(next(counter), next(counter), next(counter)))
    particle.setReferencePoint(
        edm4hep.Vector3f(next(counter), next(counter), next(counter))
    )
    particle.setCharge(next(counter))
    particle.setMass(next(counter))
    particle.setGoodnessOfPID(next(counter))
    particle.setCovMatrix([next(counter) for _ in range(10)])
    particle.setStartVertex(v)
    if args.use_pre1:
        particle.setParticleIDUsed(pid)
    particle.addToClusters(cluster)
    particle.addToTracks(track)
    particle.addToParticles(particle)
    if args.use_pre1:
        particle.addToParticleIDs(pid)
    reco_particle = particle
    frame.put(particles, "ReconstructedParticleCollection")

    v.setAssociatedParticle(reco_particle)

    # TODO: Add when the PID PR is merged
    # if not args.use_pre1:
    #     pid.setParticle(reco_particle)

    assocs = edm4hep.MCRecoParticleAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(reco_particle)
    assoc.setSim(daughter_particle)
    frame.put(assocs, "MCRecoParticleAssociationCollection")

    assocs = edm4hep.MCRecoCaloAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(calo_hit)
    assoc.setSim(simcalo_hit)
    frame.put(assocs, "MCRecoCaloAssociationCollection")

    assocs = edm4hep.MCRecoTrackerAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(tracker_hit)
    assoc.setSim(simtracker_hit)
    frame.put(assocs, "MCRecoTrackerAssociationCollection")

    assocs = edm4hep.MCRecoCaloParticleAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(calo_hit)
    assoc.setSim(daughter_particle)
    frame.put(assocs, "MCRecoCaloParticleAssociationCollection")

    assocs = edm4hep.MCRecoClusterParticleAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(cluster)
    assoc.setSim(daughter_particle)
    frame.put(assocs, "MCRecoClusterParticleAssociationCollection")

    assocs = edm4hep.MCRecoTrackParticleAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(track)
    assoc.setSim(daughter_particle)
    frame.put(assocs, "MCRecoTrackParticleAssociationCollection")

    assocs = edm4hep.RecoParticleVertexAssociationCollection()
    assoc = assocs.create()
    assoc.setWeight(next(counter))
    assoc.setRec(reco_particle)
    assoc.setVertex(v)
    frame.put(assocs, "MCRecoParticleVertexAssociationCollection")

    simiocluster = edm4hep.SimPrimaryIonizationClusterCollection()
    cluster = simiocluster.create()
    cluster.setCellID(next(counter))
    cluster.setTime(next(counter))
    cluster.setPosition(edm4hep.Vector3d(next(counter), next(counter), next(counter)))
    cluster.setType(next(counter))
    for j in range(vectorsize):
        cluster.addToElectronCellID(next(counter))
        cluster.addToElectronTime(next(counter))
        cluster.addToElectronPosition(
            edm4hep.Vector3d(next(counter), next(counter), next(counter))
        )
        cluster.addToPulseTime(next(counter))
        cluster.addToPulseAmplitude(next(counter))
    cluster.setParticle(daughter_particle)
    frame.put(simiocluster, "SimPrimaryIonizationClusterCollection")

    timeseries = edm4hep.TimeSeriesCollection()
    serie = timeseries.create()
    serie.setCellID(next(counter))
    serie.setTime(next(counter))
    serie.setInterval(next(counter))
    for j in range(vectorsize):
        serie.addToAmplitude(next(counter))
    frame.put(timeseries, "TimeSeriesCollection")

    trackerpulse = edm4hep.TrackerPulseCollection()
    pulse = trackerpulse.create()
    pulse.setCellID(next(counter))
    pulse.setTime(next(counter))
    pulse.setCharge(next(counter))
    pulse.setQuality(next(counter))
    pulse.setCovMatrix([next(counter) for _ in range(3)])
    pulse.setTimeSeries(serie)
    frame.put(trackerpulse, "TrackerPulseCollection")

    recioncluster = edm4hep.RecIonizationClusterCollection()
    cluster = recioncluster.create()
    cluster.setCellID(next(counter))
    cluster.setSignificance(next(counter))
    cluster.setType(next(counter))
    cluster.addToTrackerPulse(pulse)
    frame.put(recioncluster, "RecIonizationClusterCollection")

    recdqdx = edm4hep.RecDqdxCollection()
    dqdx = recdqdx.create()
    dqdx.setParticleType(next(counter))
    dqdx.setType(next(counter))
    for j in range(5):
        h = edm4hep.Hypothesis()
        h.chi2 = next(counter)
        h.expected = next(counter)
        h.sigma = next(counter)
        dqdx.setHypotheses(j, h)
    for j in range(vectorsize):
        hd = edm4hep.HitLevelData()
        hd.cellID = next(counter)
        hd.N = next(counter)
        hd.eDep = next(counter)
        hd.pathLength = next(counter)
        dqdx.addToHitData(hd)
    dqdx.setTrack(track)
    frame.put(recdqdx, "RecDqdxCollection")

    writer.write_frame(frame, "events")
